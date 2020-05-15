import json

from cogs.cogfunctions.database import Database
from scripts.logger import Logger
from wows.shipparam import ShipParam
from wows.warship import Warship


class Wows_database:
	"""
	Wows_database class.
	Responsible for interactions with database.
	"""
	__slots__ = ('database', 'logger')

	def __init__(self, db_path):
		self.database = Database(db_path)
		self.logger = Logger(self.__class__.__name__)
		# if db file not found or empty, create file
		try:
			with open(db_path, 'rb') as f:
				if f.read() == b'':
					self._create_table()
		except Exception as e:
			self.logger.info('Database not found.')
			self._create_table()

	def _create_table(self):
		self.logger.debug('Creating wows database table.')
		self.database.executescript("""
		CREATE TABLE players(
			discord_id INTEGER PRIMARY KEY AUTOINCREMENT,
			wows_id INTEGER,
			in_game_name TEXT,
			clan TEXT
		);
		CREATE TABLE version (
			version_id INTEGER PRIMARY KEY AUTOINCREMENT,
			ships_updated_at INTGER
		);
		CREATE TABLE updates(
			id INTEGER PRIMARY KEY AUTOINCREMENT,
			ship_id INTEGER,
			diff TEXT
		);
		CREATE TABLE warships(
			price_gold INTEGER,
			ship_id_str TEXT,
			has_demo_profile INTEGER,
			images TEXT,
			modules TEXT,
			modules_tree TEXT,
			nation TEXT,
			is_premium INTEGER,
			ship_id INTEGER PRIMARY KEY,
			price_credit INTEGER,
			default_profile TEXT,
			upgrades TEXT,
			tier INTEGER,
			next_ships TEXT,
			mod_slots INTEGER,
			type TEXT,
			is_special INTEGER,
			name TEXT
		);
		CREATE TABLE shipparams(
			engine TEXT,
			anti_aircraft TEXT,
			mobility TEXT,
			hull TEXT,
			atbas TEXT,
			artillery TEXT,
			torpedoes TEXT,
			fighters TEXT,
			ship_id INTEGER PRIMARY KEY,
			fire_control TEXT,
			weaponry TEXT,
			flight_control TEXT,
			concealment REAL,
			armour TEXT,
			dive_bomber TEXT
		);
		INSERT INTO version(ships_updated_at) VALUES('initial value');
		""")
		self.logger.debug('Created wows database table.')

	def get_db_version(self):
		"""
		Get the version of database.
		"""
		command = 'SELECT ships_updated_at from version ORDER BY version_id desc'
		result = self.database.fetch(command)
		version = result[0]
		self.logger.debug('Returning database version.')
		return version
		
	def update_version(self, version):
		"""
		Update version to given version.
		"""
		command = 'INSERT INTO version(ships_updated_at) VALUES(?)'
		self.database.execute(command, (version,))
		self.logger.debug('Database updated.')
	
	def get_warship(self, name) -> Warship:
		"""
		Get information of a warship of given name.
		If many data match, returns as list of Warship instance.
		"""
		self.logger.debug(f'Searching for a warship with {name=}.')
		# exact match
		result = self.database.fetch('SELECT * FROM warships WHERE name=?', (name,))
		if result:
			self.logger.debug('Found exact match.')
			warship = Warship.warship_from_tuple(result)
			return warship
		results = self.database.fetch(f'SELECT * FROM warships WHERE name LIKE ?', (f'{name}%',), count=3)
		self.logger.debug('Found close match.')
		warships = list(map(lambda result: Warship.warship_from_tuple(result), results))
		return warships

	def get_warships(self) -> list:
		"""
		Get list of warships as list of Warship instance.
		"""
		results = self.database.fetch('SELECT * FROM warships', count=-1)
		warships = list(map(lambda result: Warship.warship_from_tuple(result), results))
		return warships

	def get_ship_ids(self) -> list:
		"""
		Get ship ids stored in database as a list.
		"""
		result = self.database.fetch('SELECT ship_id from warships', count=-1)		
		return result

	def get_shipparam(self, ship_id) -> ShipParam:
		"""
		Get ship parameters of given ship_id.
		"""
		result = self.database.fetch('SELECT * FROM shipparams WHERE ship_id=?', (ship_id,))
		if not result:
			return None
		param = ShipParam.shipparam_from_tuple(result)
		return param
	
	def update_warship(self, warship):
		"""
		Update database with given warship.
		"""
		self.deregister_ship(warship.ship_id)
		self.register_ship(warship)

	def update_shipparam(self, param:ShipParam):
		self.deregister_shipparam(param.ship_id)
		self.register_shipparam(param)

	def register_shipparam(self, param:ShipParam):
		command = 'INSERT INTO shipparams VALUES (?,?,?,?,?,?,?,' \
			'?,?,?,?,?,?,?,?)'	
		values = param.to_tuple()
		self.database.execute(command, values)

	def deregister_shipparam(self, ship_id:int):
		command = 'DELETE FROM shipparams WHERE ship_id=?'
		values = (ship_id,)
		self.database.execute(command, values)

	def register_ship(self, warship:Warship):
		"""
		Register ship into database.
		"""
		command = 'INSERT INTO warships VALUES(?,?,?,?,?,?,?,?,?,?,' \
												'?,?,?,?,?,?,?,?)' 
		values = warship.to_tuple()
		self.database.execute(command, values)
	
	def deregister_ship(self, ship_id:int):
		"""
		Deregister warship from database.
		"""
		command = 'DELETE FROM warships WHERE ship_id=?'
		values = (ship_id,)
		self.database.execute(command, values)

	def register_user(self, player, discord_id):
		"""
		Register discord user into database.
		"""
		self.logger.debug(f'Registering {player["nickname"]}.')
		self.database.execute('INSERT INTO players VALUES(?, ?, ?, ?) ', (discord_id, player['account_id'], player['nickname'], ''))
		self.logger.debug('Registered player.')
	
	def deregister_user(self, discord_id):
		"""
		Deregister discord user from database.
		"""
		self.logger.debug('Deregistering user.')
		self.database.execute('DELETE FROM players WHERE discord_id = ?', (discord_id,))
		self.logger.debug('Deregistered user.')
	
	def is_user_registered(self, discord_id):
		"""
		Checks is given discord_id is registered.
		"""
		result = self.database.fetch('SELECT discord_id from players WHERE discord_id = ?', (discord_id,))
		self.logger.debug(f'{result=}')
		return result is not None
