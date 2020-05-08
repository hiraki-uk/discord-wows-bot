from cogs.cogfunctions.database import Database
from scripts.logger import Logger
import json

from .warship import Warship

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
	
	def get_warship(self, name):
		"""
		Get information of a warship of given name.
		"""
		self.logger.debug(f'Searching for a warship with {name=}.')
		# exact match
		result = self.database.fetch('SELECT * FROM warships WHERE name=?', (name,))
		if result:
			warship = create_warship_from_db(result)
			return warship
		results = self.database.fetch(f'SELECT * FROM warships WHERE name LIKE ?', (f'{name}%',), count=3)
		warships = []
		if results:
			for result in results:
				warship = create_warship_from_db(result)
				warships.append(warship)

		return warships

	def update_warships(self, warships):
		"""
		Update database with given warships.
		"""
		for warship in warships:
			# if id not found in database, register
			result = self.database.execute('SELECT * FROM warships WHERE ship_id=?', (warship['ship_id'],))
			if result is None:
				self.register_ship(warship)
			# if id found but data not up to date, update
			else:
				pass
				# diff = Warship.get_diff(warship, result)
				# if diff is not None:
				# 	self.save_updates(diff)
				# 	self.update_warship(warship)

	def register_ship(self, data):
		"""
		Register ship into database.
		"""
		price_gold = data['price_gold']
		ship_id_str = data['ship_id_str']
		has_demo_profile = data['has_demo_profile']
		images = data['images']
		modules = data['modules']
		modules_tree = data['modules_tree']
		nation = data['nation']
		is_premium = data['is_premium']
		ship_id = data['ship_id']
		price_credit = data['price_credit']
		default_profile = data['default_profile']
		upgrades = data['upgrades']
		tier = data['tier']
		next_ships = data['next_ships']
		mod_slots = data['mod_slots']
		shiptype = data['type']
		is_special = data['is_special']
		name = data['name']

		has_demo_profile = 1 if has_demo_profile == 'True' else 0
		images = str(images)
		modules = str(modules)
		modules_tree = str(modules_tree)
		is_premium = 1 if is_premium == 'True' else 0
		default_profile = str(default_profile)
		upgrades = str(upgrades)
		next_ships = str(next_ships)
		is_special = 1 if is_special == 'True' else 0

		command = 'INSERT INTO warships VALUES(?,?,?,?,?,?,?,?,?,?,' \
												'?,?,?,?,?,?,?,?)' 
		values = (price_gold, ship_id_str, has_demo_profile,
			images, modules, modules_tree, nation, is_premium,
			ship_id, price_credit, default_profile, upgrades,
			tier, next_ships, mod_slots, shiptype, is_special, name)
	
		self.database.execute(command, values)
		
	# def update_warship(self, warship):
	# 			command = 'INSERT INTO warships VALUES(?,?,?,?,?,?,?,?,?,?,' \
	# 											'?,?,?,?,?,?,?,?)' 
	# 	self.database.execute(command, values)	


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
