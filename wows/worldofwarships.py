import json

from wows.warship import Warship

gp_path = 'wows/gameparams.json'
ships_path = 'wows/ships.json'
ship_ids_path = 'wows/ship_ids.txt'
ship_ids_api_path = 'wows/ship_ids_api.txt'

class WorldOfWarships:
	def __init__(self):
		with open(ships_path, 'r') as f:
			s = f.read()
		self.s_json = json.loads(s)

	def create_warship(self, name:str) -> Warship:
		"""
		Create Warship instance of a given name.
		"""
		warship = Warship(self.s_json[name])
		return warship

	def search_ship_id(self, name:str):
		"""
		Search for ship_id in ship_ids_api.txt file.
		Returns ship_id if only one found, list of names if multiple hit.

		Returns
		-------
		ship_id : int
			ship_id of given name
		ship_names : list of str
			list of ship_name
		"""
		with open(ship_ids_api_path, 'r') as f:
			s = f.read()
		s_jsn = json.loads(s)
		ship_ids = {shipname:ship_id for shipname, ship_id in s_jsn.items() if name.lower() in shipname.lower()}
		if not ship_ids:
			print('None found.')
			return
		if len(ship_ids) == 1:
			print('Exact match found.')
			ship_id = ship_ids.values()[0]
			return ship_id
		else:
			print('Multiple found.')
			ship_names = [ship_name for ship_name in ship_ids.keys()]
			return ship_names

	def get_ship(self, ship_id:int):
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
		if not ships:
			return
		elif len(ships) == 1:
			ship = ships[0].strip()
			return [self.create_warship(ship), _create_name(ship)]
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