import json
import os
import time

import requests
from dotenv import load_dotenv
from wowspy import Region, Wows

env_path = '.env'
load_dotenv(dotenv_path=env_path)
key = os.getenv('WOWS_APPLICATION_ID')

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

def _create_ship_ids_str_from_api():
	"""
	Create ship_ids_str_api.txt file.
	"""
	wows = Api()
	result = wows.get_ship_id_str_pages()
	if result is None: return
	ships = {}
	for page in range(result):
		result = wows.get_ship_ids_str(page+1)
		if result is None: return
		ships.update(result)

	with open('ship_ids_str_api.txt', 'w', encoding='utf-8') as f:
		f.write(json.dumps(ships, indent=4).encode().decode('unicode-escape'))
	print('Done.')


class Api:
	def __init__(self):
		self._base = 'https://api.worldofwarships.asia/wows/encyclopedia/ships/?application_id={}&fields={}&language=en&page_no={}'

	def get_ship_id_str_pages(self):
		"""
		Get how many ship_id_str pages you need to fetch.
		
		Returns
		-------
		pages : int
		"""
		time.sleep(0.1)
		result = requests.get(self._base.format(key, 'ship_id_str', 1))
		if result.status_code != 200: return
		text = result.text
		temp = json.loads(text)
		if temp['status'] != 'ok': return
		pages = temp['meta']['page_total']
		return pages

	def get_ship_ids_str(self, page:int):
		"""
		Get ship_ids_str from api as dict.
		
		Returns
		-------
		data : dict
			{'name1':'ship_id_str1', 'name2':'ship_id_str2', ...}
		"""
		time.sleep(0.1)
		result = requests.get(self._base.format(key, 'name,ship_id_str', page))
		if result.status_code != 200: return
		text = result.text
		temp = json.loads(text)
		if temp['status'] != 'ok': return
		data = {v['name']:v['ship_id_str'] for k, v in temp['data'].items()}
		return data
		

if __name__ == '__main__':
	# _create_ship_ids_from_api()
	# Api().get_ship_ids(1)
	_create_ship_ids_str_from_api()
