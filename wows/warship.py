from discord import Embed


class Warship:
	def __init__(self, data):
		price_gold = data['price_gold']
		ship_id_str = data['ship_id_str']
		has_demo_profile = data['has_demo_profile']
		images = data['images']
		modules = data['modules']
		modules_tree = data['modules_tree']
		nation = data['nation']
		is_premium = data['is_premium']
		ship_id = data['ship_id']
		price_credit = data['price_credit']
		default_profile = data['default_profile']
		upgrades = data['upgrades']
		tier = data['tier']
		next_ships = data['next_ships']
		mod_slots = data['mod_slots']
		shiptype = data['type']
		is_special = data['is_special']
		name = data['name']

		has_demo_profile = 1 if has_demo_profile == 'True' else 0
		images = str(images)
		modules = str(modules)
		modules_tree = str(modules_tree)
		is_premium = 1 if is_premium == 'True' else 0
		default_profile = str(default_profile)
		upgrades = str(upgrades)
		next_ships = str(next_ships)
		is_special = 1 if is_special == 'True' else 0

		self.warship = (price_gold, ship_id_str, has_demo_profile,
			images, modules, modules_tree, nation, is_premium,
			ship_id, price_credit, default_profile, upgrades,
			tier, next_ships, mod_slots, shiptype, is_special, name)
		self.warship_dict = {
			'price_gold':price_gold,
			'ship_id_str':ship_id_str,
			'has_demo_profile':has_demo_profile,
			'images':images,
			'modules': modules,
			'modules_tree': modules_tree,
			'nation': nation,
			'is_premium': is_premium,
			'ship_id':ship_id,
			'price_credit':price_credit,
			'default_profile':default_profile,
			'upgrades': upgrades,
			'tier':tier,
			'next_ships':next_ships,
			'mod_slots': mod_slots,
			'shiptype': shiptype,
			'is_special': is_special,
			'name': name
		}

	def embed_builder(self):
		embed = Embed(colour=0x793DB6)
		a = embed.add_field
		d = self.warship_dict
		a(name=d['name'], value=f'T{d["tier"]} {d["nation"][:2]} {d["shiptype"]}')
		# a(name=)

		return embed

	@staticmethod
	def get_diff(warship1:tuple, warship2:tuple):
		"""
		Get the difference of two warships.
		"""
		pass

	@staticmethod
	def get_ship_from_data(data:dict):
		"""
		Create Warship instance from data.
		"""
		pass
	
	@staticmethod
	def create_ship_from_db(data:tuple):
		"""
		Create warship instance from tuple gained from database.
		"""
		pass