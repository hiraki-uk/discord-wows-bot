import json

from utils.database import Database

from ..api.api_db import ApiDB
from ..gp.gp_db import GameparamsDB
from ..i18n.i18n_db import I18NDb
from .warship import Warship

path = 'res/warships.db'


def create_warships_db():
	apidb = ApiDB()
	gpm = GameparamsDB()
	warshipdb = WarshipDB()
	i18n = I18NDb()
	warshipdb.init_db()

	ship_ids = apidb.list_all_ships()
	ships = []
	for name, ship_id_str in ship_ids:
		ship = gpm.search_ship(ship_id_str, i18n)
		ships.append((ship, name))
	warshipdb.insert_data(ships)


class WarshipDB:
	def __init__(self) -> None:
		self.db = Database(path)
		self.i18ndb = I18NDb() 
	

	def init_db(self):
		"""
		Initialize database.
		"""
		# clear data
		with open(path, 'w') as f:
			f.write('')
		
		# create table
		command = 'CREATE TABLE warship(' \
			'nickname TEXT,' \
			'idx TEXT,' \
			'shipid INTEGER PRIMARY KEY,' \
			'tier INTGER,' \
			'species TEXT,' \
			'nation TEXT,' \
			'mods TEXT,' \
			'artilleries TEXT,' \
			'engines TEXT,' \
			'firecontrols TEXT,' \
			'hulls TEXT,' \
			'torpedoes TEXT)'
		self.db.execute(command)
		

	def insert_data(self, ships:list):
		"""
		Insert data into database.

		Params
		------
		ships : list
			list of ships.
		"""
		# list for command, value
		l = []
		for ship, nickname in ships:
			# some ships not implemented yet
			if not ship:
				continue
			# get ships' name
			values = (
				nickname,
				ship.index,
				ship.shipid,
				ship.tier,
				ship.species,
				ship.nation,
				json.dumps(ship.mods, indent=4),
				json.dumps(ship.artilleries, indent=4),
				json.dumps(ship.engines, indent=4),
				json.dumps(ship.firecontrols, indent=4),
				json.dumps(ship.hulls, indent=4),
				json.dumps(ship.torpedoes, indent=4))
			command = 'INSERT INTO warship(' \
				'nickname,' \
				'idx,' \
				'shipid,' \
				'tier,' \
				'species,' \
				'nation,' \
				'mods,' \
				'artilleries,' \
				'engines,' \
				'firecontrols,' \
				'hulls,' \
				'torpedoes) VALUES (?,?,?,?,?,?,?,?,?,?,?,?)'
			l.append((command, values))
		self.db.insertmany(l)


	def get_warship(self, command, value):
		"""
		Returns warship of given command.
		Expects an exact match, else returns None.

		Params
		------
		command : str
			e.g. SELECT * FROM warship WHERE nickname=?
		
		Returns
		-------
		warship : Warship
			Warship instance of fetched data.
		
		None
			Returned if multiple hit, or no hit.

		"""
		results = self.db.fetchall(command, value)
		# return if no results
		if results is None:
			return None
		# if exact match, return that
		if len(results) == 1:
			warship = Warship.from_tuple(results[0])
			return warship
		# multiple hits, return none
		return None
