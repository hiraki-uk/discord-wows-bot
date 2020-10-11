import json

from wows.modules import get_torp
from wows.warship import Warship


gp_path = 'wows/gameparams.json'
ships_path = 'wows/ships.json'
ship_ids_path = 'wows/ship_ids.txt'
ship_ids_str_api_path = 'wows/ship_ids_str_api.txt'


class WorldOfWarships:
	def __init__(self):
		with open(ships_path, 'r') as f:
			s = f.read()
		self.s_json = json.loads(s)

	def search_ship_id_str(self, name:str):
		"""
		Search for ship_id_str in ship_ids_str_api.txt file.
		Returns ship_id_str if only one found, list of names if multiple hit.

		Returns
		-------
		ship_id_str : str
			ship_id_str of given name
		ship_names : list of str
			list of ship_name
		"""
		with open(ship_ids_str_api_path, 'r', encoding='utf-8') as f:
			s = f.read()
		s_jsn = json.loads(s)
		ship_ids_str = {shipname:ship_id_str for shipname, ship_id_str in s_jsn.items() if name.lower() in shipname.lower() and '[' not in shipname}
		if not ship_ids_str:
			print('None found.')
			return
		if len(ship_ids_str) == 1:
			print('Exact match found.')
			ship_id_str = list(ship_ids_str.values())[0] # change from dict_values to list for slicing
			return ship_id_str
		else:
			print('Multiple found.')
			# remove rental ships
			ship_names = [ship_name for ship_name in ship_ids_str.keys()]
			# search for exact match
			for ship_name in ship_names:
				if ship_name.lower() == name.lower():
					# exact match
					print('Found exact match.')
					ship_id_str = ship_ids_str[ship_name]
					return ship_id_str
			return ship_names

	def get_ship(self, ship_id_str:str, v=False):
		"""
		Search for Warship instance of a given ship_id_str.

		Returns
		-------
		ship : Warship
			Warship instance of given ship_id_str.
		"""
		with open(ship_ids_path, 'r') as f:
			s = f.readlines()
		ships = [line.strip() for line in s if ship_id_str.lower() in line.lower()]
		if not ships:
			return
		elif len(ships) == 1:
			if not v:
				ship = Warship(self.s_json[ships[0]])
				return 	ship
			else:
				return self.s_json[ships[0]]
		return


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
