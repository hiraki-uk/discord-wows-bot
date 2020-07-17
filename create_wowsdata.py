import json

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
