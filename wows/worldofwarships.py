import json

from wows.warship import Warship

gp_path = 'wows/gameparams.json'
ships_path = 'wows/ships.json'
ship_ids_path = 'wows/ship_ids.txt'


def _ships_from_gameparams():
	with open(gp_path, 'r') as f:
		s = f.read()
	s_jsn = json.loads(s)
	ships_json = {}

	for param_key, param_value in s_jsn.items():
		try:
			if param_value['typeinfo']['type'] == 'Ship':
				ships_json[param_key] = param_value
				print(f'Found {param_key}.')
		except:
			print('Typeinfo key not found.')

	with open(ships_path, 'w') as f:
		f.write(json.dumps(ships_json, indent=4))

def _ship_ids_froms_ships():
	with open(ships_path, 'r') as f:
		s = f.read()
	s_json = json.loads(s)
	ship_ids = [ship_id for ship_id in s_json.keys()]
	with open(ship_ids_path, 'w') as f:
		f.write('\n'.join(ship_ids))

def _clean_data():
	with open(ships_path, 'r') as f:
		s = f.read()
	s_json = json.loads(s)
	for key, value in s_json.items():
		l = ['AIParams', 'A_Directors', 'Cameras', 'DockCamera', 'ShipAbilities', 'UnderwaterCamera']
		for i in range(len(l)):
			try:
				del value[l[i]]
			except Exception as e:
				pass
	with open('clean_ships.json', 'w') as f:
		f.write(json.dumps(s_json, indent=4))

def create_warship(name:str) -> Warship:
	"""
	Create Warship instance of a given name.
	"""
	with open(ships_path, 'r') as f:
		s = f.read()
	s_json = json.loads(s)
	warship = Warship(s_json[name])
	return warship

def search_ship(name:str):
	"""
	Search for Warship instance of a given name.
	Returns list of names if multiple results found.

	Returns
	-------
	result_list: list of warship and name
	name_list: list of str
	"""
	with open(ship_ids_path, 'r') as f:
		s = f.readlines()
	ships = [line for line in s if name.lower() in line.lower()]
	if ships == 0:
		return
	elif len(ships) == 1:
		ship = ships[0].strip()
		return [create_warship(ship), _create_name(ship)]
	return list(map(lambda x:_create_name(x), ships)) 
	
def _create_name(name):
	d = ''
	r = name[1] # region
	if r == 'A':
		d += '米'
	elif r == 'B':
		d += '英'
	elif r == 'F':
		d+= '仏'
	elif r == 'G':
		d += '独'
	elif r == 'I':
		d += '伊'
	elif r == 'J':
		d += '日'
	elif r == 'R':
		d += '露'
	elif r == 'U':
		d += 'イギリス連邦'
	elif r == 'V':
		d += 'パンアメリカ'
	elif r == 'W':
		d += 'パンヨーロッパ'
	elif r == 'Z':
		d += 'パンアジア'
	elif r == 'X':
		d += 'イベント'

	t = name[2:4] # type
	if t == 'SA':
		d+= '空'
	elif t == 'SB':
		d += '戦'	
	elif t == 'SC':
		d += '巡'	
	elif t == 'SD':
		d += '駆'	
	elif t == 'SS':
		d += '潜'
	return d + name[4:].strip()