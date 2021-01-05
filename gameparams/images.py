import io
from os import terminal_size
import pickle

from PIL import Image, ImageDraw, ImageEnhance, ImageFont

from gameparams.warship import Warship

base_path = 'res/base.jpeg'
output_path = 'res/temp.jpg'

font_path = 'c://windows/fonts/yumin.ttf'
font_size = 28
font_color = (255, 255, 255)


def process_image(binary_img, warship):
	"""
	Return binary final image of given binary image and warship.

	Params
	------
	binary_img : binary
		binary image of size 1920, 1080.
	warship : Warship
		warship instance.

	Returns
	------
	final_img : binary
		binary image after process. 
	"""
	img = Image.open(io.BytesIO(binary_img))
	img = img.convert('RGB')
	enhancer = ImageEnhance.Brightness(img)
	img_enh = enhancer.enhance(0.25)
	img_enh = img_enh.resize((1920, 1080))
	final_img = create_image(img_enh, warship) 
	return final_img


def add_text(img, text, font_path, font_size, font_color, height, width):
	pos = (width, height)
	font = ImageFont.truetype(font_path, font_size)
	draw = ImageDraw.Draw(img)
	draw.text(pos, text, font_color, font=font)


def add_shipname(base, name, description):
	"""
	Adds shipname and description to base. Returns position for next text.
	"""
	shipname = name
	shipname_size = 100
	color = (255, 255, 255)
	height = 10
	width = 25
	add_text(base, shipname, font_path, shipname_size, color, height, width)

	height += shipname_size + 10
	add_text(base, description, font_path, font_size, font_color, height, width)
	return height + font_size + 20, width


def add_descriptions(base, title, descriptions, height, width):
	"""
	Adds hull description to base. Returns height for next text to add.
	"""
	title_size = 48
	add_text(base, title, font_path, title_size, font_color, height, width)
	height += title_size + 5
	height, width = get_pos(height, width)

	for description in descriptions:
		add_text(base, description, font_path, font_size, font_color, height, width)
		count = description.count('\n')
		if count:
			height += font_size * (count + 1) + 15
		else:
			height += font_size + 15
		height, width = get_pos(height, width)
	return height + 10, width


def get_pos(height, width):
	"""
	Check position.
	"""
	if width == 900: # give up 
		return height, width
	if height < 1000:
		return height, width
	if 1000 <= height:
		return 150, 900


def create_mod_text(l:list):
	text = ''
	count = len(l) // 2
	for i in range(count):
		text += ', '.join(l[i*2 : (i+1)*2]) + '\n'
	rmd = len(l) % 2
	for i in range(rmd):
		text += ', '.join(l[count*2:])
	return text


def create_image(base, warship:Warship):
	"""
	Creates description image of given warship.
	"""
	name = warship.name
	description=f'T{warship.tier} {warship.nation[:2].upper()} {warship.species},　shipID {warship.shipid}'
	height, width = add_shipname(base, name, description)

	if warship.hulls:
		title = '船体'
		descriptions = []
		for hull in warship.hulls:
			if warship.tier > 7 or \
				'Belfast' in warship.name or \
				'Z-39' in warship.name:
				best_concealment_ship = round(hull["visibility"] * 0.9 * 0.9 * 0.97, 2)
				best_concealment_plane = round(hull['visibility_plane'] * 0.9 * 0.9 * 0.97, 2)
			else:
				best_concealment_ship = round(hull["visibility"] * 0.9 * 0.97, 2)
				best_concealment_plane = round(hull['visibility_plane'] * 0.9 * 0.97, 2)

			descriptions.append(f'体力 {round(hull["health"])}　（{round(hull["health"])+350*warship.tier}）　最良隠蔽{best_concealment_ship}km　航空{best_concealment_plane}km\n' \
				f'速力{hull["max_speed"]}kts　全長{hull["size"]}m　旋回半径{hull["turning_radius"]}m')
		height, width = add_descriptions(base, title, descriptions, height, width)

	if warship.artilleries:
		title = '主砲'
		descriptions = []
		for artillery in warship.artilleries:
			numbarrels = 0
			rotation_speed = 0
			shotdelay = 0
			barrelDiameter = 0
			ammunition = ''
			for ammo in artillery['ammolist']:
				if ammo['ammotype'] == 'HE':
					ammunition += f'HE　{ammo["speed"]}m/s　火災{round(ammo["burnprob"]*100)}%　{ammo["alphadmg"]}dmg\n'
				elif ammo['ammotype'] == 'AP':
					ammunition += f'AP　{ammo["speed"]}m/s　跳弾開始{ammo["ricochet"]}度　{ammo["alphadmg"]}dmg\n'
				elif ammo['ammotype'] == 'CS':
					ammunition += f'CS　{ammo["speed"]}m/s　跳弾開始{ammo["ricochet"]}度　{ammo["alphadmg"]}dmg\n'
				else:
					ammunition += f'{ammo["ammotype"]}　{ammo["speed"]}m/s　跳弾開始{ammo["ricochet"]}度　火災{round(ammo["burnprob"]*100)}%　{ammo["alphadmg"]}dmg\n'
			for gun in artillery['guns']:

				barrelDiameter = gun['barrelDiameter']
				numbarrels += gun['numBarrels']
				rotation_speed = gun['rotationSpeed']
				shotdelay = gun['shotDelay']
			descriptions.append(f'{round(barrelDiameter*1000)}mm砲　{len(artillery["guns"])}基　{round(numbarrels)}門　' \
				f'装填{shotdelay}s　180度旋回{rotation_speed}s　σ{artillery["sigma"]}\n'+ammunition)
		height, width = add_descriptions(base, title, descriptions, height, width)

	if warship.torpedoes:
		title = '魚雷'
		descriptions = []
		for torp in warship.torpedoes:
			torp_info = None
			for gun in torp['guns']:
				torp_info = ''
				for tp in gun['torps']:
					torp_info += f'{round(tp["maxDist"], 1)}km　{tp["speed"]}kts　被発見{tp["visibility"]}km　{tp["dmg"]}dmg\n'
				break
			numbarrels = sum(map(lambda x:x['numBarrels'], torp['guns']))
			shotdelay = torp['guns'][0]['shotDelay']
			descriptions.append(f'{len(torp["guns"])}基{numbarrels}門　装填{shotdelay}s　{torp_info}')
		height, width = add_descriptions(base, title, descriptions, height, width)

	if warship.firecontrols:
		title = '射撃管制装置'
		descriptions=[(',　'.join(list(map(
			lambda firecontrol:f'射程{round(artillery["maxDist"] * firecontrol / 1000, 2)}km',
			warship.firecontrols
		))))]
		height, width = add_descriptions(base, title, descriptions, height, width)

	mod_slot = 1
	for mods in warship.mods:
		# return if empty
		if not mods:
			break
		# for every mod, add to description
		title = f'UGスロット{mod_slot}'
		descriptions = []
		for mod in mods:
			descriptions.append(f'{mod["name"][7:]}')
			
		mod_slot += 1
		descriptions = [create_mod_text(descriptions)]
		height, width = add_descriptions(base, title, descriptions, height, width)

	base.save(output_path)
	with open(output_path, 'rb') as f:
		binary_img = f.read()
	return binary_img