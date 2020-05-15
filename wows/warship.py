from discord import Embed


class Warship:
	def __init__(self, data):
		self.price_gold = data['price_gold']
		self.ship_id_str = data['ship_id_str']
		self.has_demo_profile = data['has_demo_profile']
		self.images = data['images']
		self.modules = data['modules']
		self.modules_tree = data['modules_tree']
		self.nation = data['nation']
		self.is_premium = data['is_premium']
		self.ship_id = data['ship_id']
		self.price_credit = data['price_credit']
		self.default_profile = data['default_profile']
		self.upgrades = data['upgrades']
		self.tier = data['tier']
		self.next_ships = data['next_ships']
		self.mod_slots = data['mod_slots']
		self.shiptype = data['type']
		self.is_special = data['is_special']
		self.name = data['name']

		# override above data
		self.has_demo_profile = 1 if self.has_demo_profile == 'True' else 0
		self.images = str(self.images)
		self.modules = str(self.modules)
		self.modules_tree = str(self.modules_tree)
		self.is_premium = 1 if self.is_premium == 'True' else 0
		self.default_profile = str(self.default_profile)
		self.upgrades = str(self.upgrades)
		self.next_ships = str(self.next_ships)
		self.is_special = 1 if self.is_special == 'True' else 0

	def __eq__(self, obj):
		return isinstance(obj, Warship) and self.to_tuple() == obj.to_tuple()

	def __ne__(self, obj):
		return not self == obj

	def to_tuple(self):
		warship_tuple = (self.price_gold, self.ship_id_str, self.has_demo_profile,
			self.images, self.modules, self.modules_tree, self.nation, self.is_premium,
			self.ship_id, self.price_credit, self.default_profile, self.upgrades,
			self.tier, self.next_ships, self.mod_slots, self.shiptype, self.is_special, self.name)
		return warship_tuple
	
	def to_dict(self):
		warship_dict = {
			'price_gold': self.price_gold,
			'ship_id_str': self.ship_id_str,
			'has_demo_profile': self.has_demo_profile,
			'images': self.images,
			'modules': self.modules,
			'modules_tree': self.modules_tree,
			'nation': self.nation,
			'is_premium': self.is_premium,
			'ship_id': self.ship_id,
			'price_credit': self.price_credit,
			'default_profile': self.default_profile,
			'upgrades': self.upgrades,
			'tier': self.tier,
			'next_ships': self.next_ships,
			'mod_slots': self.mod_slots,
			'shiptype': self.shiptype,
			'is_special': self.is_special,
			'name': self.name
		}
		return warship_dict

	def embed_builder(self):
		embed = Embed(colour=0x793DB6)
		a = embed.add_field
		d = self.warship_dict
		a(name=d['name'], value=f'T{d["tier"]} {d["nation"][:2]} {d["shiptype"]}')
		# a(name=)

		return embed

	@staticmethod
	def warship_from_tuple(data:tuple):
		"""
		Create warship instance from tuple.
		"""
		if data is None:
			return None
		warship_dict = {
			'price_gold': data[0],
			'ship_id_str': data[1],
			'has_demo_profile': data[2],
			'images': data[3],
			'modules': data[4],
			'modules_tree': data[5],
			'nation': data[6],
			'is_premium': data[7],
			'ship_id': data[8],
			'price_credit': data[9],
			'default_profile': data[10],
			'upgrades': data[11],
			'tier': data[12],
			'next_ships': data[13],
			'mod_slots': data[14],
			'shiptype': data[15],
			'is_special': data[16],
			'name': data[17]
		}
		warship = Warship(warship_dict)
		return warship
		
	@staticmethod
	def warship_from_dict(data:dict):
		"""
		Create Warship instance from dict.
		"""
		warship = Warship(data)
		return warship