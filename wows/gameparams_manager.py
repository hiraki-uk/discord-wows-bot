import ast

from utils.database import Database

from wows.warship import Warship


db_path = 'wows/gameparams.db'
id_api_db_path = 'wows/id_api.db'


class GP_Manager:
	def __init__(self) -> None:
		self.db = Database(db_path) 
		self.id_api_db = Database(id_api_db_path)
	

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
			ship_names = [ship[0] for ship in ship_list]
			return ship_names


	def search_ship(self, index_str:str, v=False):
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
		data = ast.literal_eval(result)
		if v:
			return data
		ship = Warship(data, self)
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
		data = ast.literal_eval(result)
		return data