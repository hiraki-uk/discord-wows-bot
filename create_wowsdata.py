"""
Creates GameParams.json related files.
gameparams.json file needed.
"""
import json
import os
import sqlite3
import time

import requests
from dotenv import load_dotenv
from wowspy import Region, Wows

from utils.database import Database

env_path = '.env'
load_dotenv(dotenv_path=env_path)
key = os.getenv('WOWS_APPLICATION_ID')

gp_json_path = 'wows/gameparams.json'
gp_db_path = 'wows/gameparams.db'
ip_api_db_path = 'wows/id_api.db'

def create_gameparams_db():
	with open(gp_json_path, 'r') as f:
		s = f.read()
	s_json = json.loads(s)
	nation = []
	species = []
	types = []
	others = []
	for key, value in s_json.items():
		temp = value['typeinfo']
		for key1, value1 in temp.items():
			# if nation
			if key1 == 'nation':
				if not value1 in nation:
					# if none use string none
					if value1 is None:
						if 'None' not in species:
							species.append('None')               
					nation.append(value1)
			# species
			elif key1 == 'species':
				if value1 not in species:
					# if none use string none
					if value1 is None:
						if 'None' not in species:
							species.append('None')               
					else:
						species.append(value1)
			# type
			elif key1 == 'type':
				if value1 not in types:
					# if none use string none
					if value1 is None:
						if 'None' not in species:
							species.append('None')               
					types.append(value1) 
	conn = sqlite3.connect(gp_db_path)
	c = conn.cursor()
	for specie in species:
		# removing errors
		specie = specie.replace(' ', '')
		if specie == 'Drop':
			specie = 'Drop_'
		c.execute(f'drop table if exists {specie}')
		command = f"""create table {specie} (
		id INTEGER PRIMARY KEY,
		index_str TEXT,
		name TEXT,
		data TEXT)"""
		c.execute(command)
	conn.commit()
	conn.close()

	conn = sqlite3.connect(gp_db_path)
	c = conn.cursor()
	for key, value in s_json.items():
		specie = value['typeinfo']['species']
		if specie is None:
			specie = 'None'
		specie = specie.replace(' ', '')
		if specie == 'Drop':
			specie = 'Drop_' 
		
		id_ = value['id']
		index = value['index']
		name = value['name']
		data = str(value)
		command = f'insert into {specie} (id, index_str, name, data) values (?, ?, ?, ?)'
		c.execute(command, (id_, index, name, data))
	conn.commit()
	conn.close()


def _create_id_api_db():
	"""
	Create id_api.db file.
	"""
	db = Database(ip_api_db_path)
	db.execute('DROP TABLE IF EXISTS ships')
	
	wows = Api()
	result = wows.get_ship_id_str_pages()
	if result is None: return
	ships = {}
	for page in range(result):
		result = wows.get_ship_ids_str(page+1)
		if result is None: return
		ships.update(result)

	db.executescript("""CREATE TABLE ships(
		id_int INTEGER PRIMARY KEY AUTOINCREMENT,
		name TEXT,
		id_str TEXT)""")
	for name, id_str in ships.items():
		db.execute('INSERT INTO ships (name, id_str) VALUES (?, ?)', (name, id_str))


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
		

def init_db():
	"""
	Initialize databases.
	"""
	with open(gp_db_path, 'w'):
		pass
	with open(ip_api_db_path, 'w'):
		pass


if __name__ == '__main__':
	init_db()
	_create_id_api_db()
	create_gameparams_db()