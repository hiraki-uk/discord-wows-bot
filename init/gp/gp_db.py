import json

from utils.database import Database

from .artillery import Artillery
from .module import Module
from ..warship.warship import Warship

db_path = 'res/gameparams.db'
id_api_db_path = 'res/id_api.db'
gp_json_path = 'res/gameparams.json'


def create_gp_db():
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


class GameparamsDB:
	def __init__(self) -> None:
		self.db = Database(db_path) 
		self.id_api_db = Database(id_api_db_path)


	def init_db(self, species):
		# list for commands
		l = []
		for specie in species:
			# removing errors
			specie = specie.replace(' ', '')
			if specie == 'Drop':
				specie = 'Drop_'
			# drop table then create
			self.db.execute(f'drop table if exists {specie}')
			command = f"""create table {specie} (
			id INTEGER PRIMARY KEY AUTOINCREMENT,
			index_str TEXT,
			name TEXT,
			data TEXT)"""
			l.append(command)
		self.db.executemany(l)


	def insert_data(self, s_json):
		# list for storing command, value
		l = []
		for value in s_json.values():
			specie = value['typeinfo']['species']
			if specie is None:
				specie = 'None'
			specie = specie.replace(' ', '')
			if specie == 'Drop':
				specie = 'Drop_' 
			
			id_ = value['id']
			index = value['index']
			name = value['name']
			command = f'insert into {specie} (id, index_str, name, data) values (?, ?, ?, ?)'
			# save raw data
			data = json.dumps(value, indent=4)
			l.append((command, (id_, index, name, data)))
		self.db.insertmany(l)


	def search_ship_id_str(self, name:str):
		"""
		Search for ship_id_str in api_db.
		Returns ship_id_str if only one found, list of names if multiple hit.

		Returns
		-------
		ship_id_str : str
			ship_id_str of given name
		ship_names : list of str
			list of ship_name
		"""
		command = f'SELECT name, id_str FROM ships WHERE name like "%{name}%"'
		results = self.id_api_db.fetchall(command) # ((name, id), (name, id), (name, id))
		ship_list = [(result[0], result[1]) for result in results if name.lower() in result[0].lower() 
			and '[' not in result[0].lower()
			and 'ARP' not in result[0]
			and not result[0].endswith(' B')]

		if not ship_list:
			return
		if len(ship_list) == 1:
			ship_id_str = ship_list[0][1] # index 0 of list, index 1 of tuple
			return ship_id_str
		else:
			# check for exact match
			for ship in ship_list:
				if name.lower() == ship[0].lower():
					return ship[1]
			ship_names = [ship[0] for ship in ship_list]
			return ship_names


	def search_ship(self, index_str:str, i18n, v=False):
		"""
		Search for ship with given index_str.
		
		Params
		------
		index_str : str
			Index string of a ship. E.g. PJSB918

		Returns
		-------
		ship : Warship
			Warship instance of specified ship.
		"""
		# search through tables
		result = None
		tables = ['Battleship', 'Cruiser', 'Destroyer', 'AirCarrier', 'Submarine']
		for table in tables:
			command = f'SELECT data FROM {table} WHERE index_str=?'
			result = self.db.fetchone(command, values=(index_str,))
			if result:
				break
		if not result:
			return
		# return data
		result = result[0]
		data = json.loads(result)
		if v:
			return data
		ship = Warship.from_params(self, i18n, data)
		return ship


	def search_torp(self, name:str):
		"""
		Search for torp with given name.
		
		Params
		------
		name : str
			Index stirng of a torp. E.g. PJPT001_Sea_Torpedo_Type93
		
		Returns
		-------
		torp : json
			json of given torp.
		"""
		# search for torp
		command = f'SELECT data FROM Torpedo WHERE name=?'
		result = self.db.fetchone(command, values=(name,))
		if not result:
			return
		result = result[0]
		data = json.loads(result)
		return data
	

	def search_artillery(self, name:str):
		command = f'SELECT data FROM Artillery WHERE name=?'
		result = self.db.fetchone(command, values=(name,))
		if not result:
			return
		result = result[0]
		data =json.loads(result)
		artillery = Artillery.from_data(data)
		return artillery


	def get_all_mods(self):
		"""
		Get all mods from database.

		Returns
		-------
		mods : List of Module
			List of Module instances.
		"""
		command = f'SELECT data FROM None WHERE index_str like "PCM%"'
		result = self.db.fetchall(command)
		if not result:
			return
		# create 
		mods = []
		for res in result:
			res = res[0]
			data = json.loads(res)
			mod = Module.from_data(data)
			mods.append(mod)
			
		return mods