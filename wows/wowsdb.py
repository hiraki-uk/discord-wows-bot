from cogs.cogfunctions.database import Database
from scripts.logger import Logger
import json

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
		CREATE TABLE warships(
			price_gold INTEGER,
			ship_id_str TEXT,
			has_demo_profile INTEGER,
			images TEXT,
			modules TEXT,
			modules_tree TEXT,
			nation TEXT,
			is_premium INTEGER,
			ship_id INTEGER,
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
		""")
		self.logger.debug('Created wows database table.')

	def _fill_database(self):
		"""
		Fill database with warships.
		"""
	def register_ship(self, data):
		"""
		Register ship into database only if 
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
		upgrades = data['upgrages']
		tier = data['tier']
		next_ships = data['next_ships']
		mod_slots = data['mod_slots']
		shiptype = data['type']
		is_special = data['is_special']
		name = data['name']

		has_demo_profile is 1 if has_demo_profile == 'true' else 0
		images = str(images)
		modules = str(modules)
		modules_tree = str(modules_tree)
		
		command = 'INSERT INTO warships VALUES(?,?,?,?,?,?,?,?,?,?,' \
												'?,?,?,?,?,?,?,?)' 
		values = (price_gold, ship_id_str, has_demo_profile,
			images, modules, modules_tree, nation, is_premium,
			ship_id, price_credit, default_profile, upgrades,
			tier, next_ships, mod_slots, shiptype, is_special, name)
	
		self.database.execute(command, values)
		
	def register(self, player, discord_id):
		"""
		Register discord user into database.
		"""
		self.logger.debug(f'Registering {player["nickname"]}.')
		self.database.execute('INSERT INTO players VALUES(?, ?, ?, ?) ', (discord_id, player['account_id'], player['nickname'], ''))
		self.logger.debug('Registered player.')
	
	def deregister(self, discord_id):
		"""
		Deregister discord user from database.
		"""
		self.logger.debug('Deregistering user.')
		self.database.execute('DELETE FROM players WHERE discord_id = ?', (discord_id,))
		self.logger.debug('Deregistered user.')
	
	def is_registered(self, discord_id):
		"""
		Checks is given discord_id is registered.
		"""
		result = self.database.fetchone('SELECT discord_id from players WHERE discord_id = ?', (discord_id,))
		self.logger.debug(f'{result=}')
		return result is not None
