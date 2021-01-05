"""
Creates GameParams.json related files.
gameparams.json file needed.
"""
import json

from gameparams.api import Api
from gameparams.api_db import ApiDB
from gameparams.gp_db import GameparamsDB
from gameparams.warship_db import WarshipDB

gp_json_path = 'res/gameparams.json'
gp_db_path = 'res/gameparams.db'
ip_api_db_path = 'res/id_api.db'


def craete_raw_gp_db():
	with open(gp_json_path, 'r') as f:
		s = f.read()
	s_json = json.loads(s)
	# get table names
	species = []
	for _, value in s_json.items():
		temp = value['typeinfo']
		for key1, value1 in temp.items():
			if key1 == 'species':
				if value1 not in species:
					# if none use string none
					if value1 is None:
						if 'None' not in species:
							species.append('None')               
					else:
						species.append(value1)
	# for storing raw data
	db = GameparamsDB()
	db.init_db(species)
	db.insert_data(s_json)


def create_warships_db():
	# for storing processed data
	apidb = ApiDB()
	gpm = GameparamsDB()
	warshipdb = WarshipDB()
	warshipdb.init_db()

	ship_ids = apidb.list_all_ships()
	ships = []
	for name, ship_id_str in ship_ids:
		ship = gpm.search_ship(ship_id_str)
		ships.append((ship, name))
	warshipdb.insert_data(ships)


def create_image_db():
	shipsdb = WarshipDB()
	db = ApiDB()
	db.process_images(shipsdb)


def create_api_info():
	"""
	Create id_api.db file.
	"""
	wows = Api()
	db = ApiDB()
	db.init_db()
	
	result = wows.get_ship_id_str_pages()
	if result is None: return
	ships = []
	for page in range(result):
		result = wows.fetch_ship_info(page+1)
		if result is None: return
		ships.extend(result)
	db.insert_data(ships)


if __name__ == '__main__':
	create_api_info()
	print('done.')
	craete_raw_gp_db()
	print('done.')
	create_warships_db()
	print('done.')
	create_image_db()
	print('Done.')