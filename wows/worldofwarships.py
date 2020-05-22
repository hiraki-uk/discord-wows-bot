import math

from tqdm import tqdm

from scripts.logger import Logger
from wows.wowsapi import WowsApi
from wows.wowsdb import Wows_database


class WorldofWarships:
	def __init__(self, key, db_path):
		self.logger = Logger(self.__class__.__name__)
		self.logger.debug('Initializing wows class.')
		self.wowsapi = WowsApi(key)
		self.wowsdb = Wows_database(db_path)

	def update(self):
		# check version
		version_db = self.wowsdb.get_db_version()
		version_api = self.wowsapi.get_api_version()

		# return if version is up to date.
		if version_db == version_api:
			self.logger.debug(f'Returning as database has latest version {version_db}.')
			return
		self.update_warships()
		self.update_shipparams()

		# finally update version
		self.wowsdb.update_version(version_api)

	def update_warships(self):
		"""
		Update warships table in database.
		"""
		self.logger.debug('Updating warships in database.')
		warships_count = self.wowsapi.get_warships_count()
		pages = math.ceil(warships_count / 100)

		warships_api = self.wowsapi.get_warships(pages)
		warships_db = self.wowsdb.get_warships()
		warships_db_ids = list(map(lambda warship:warship.ship_id, warships_db))

		for warship in warships_api:
			# if warship not found in db, register
			if warship.ship_id not in warships_db_ids:
				self.wowsdb.register_ship(warship)
			else:
				index = warships_db_ids.index(warship.ship_id)
				warship_db = warships_db[index]
				assert warship.ship_id == warship_db.ship_id
				# if warship from api differes from warship in db, update
				if warship != warship_db:
					self.wowsdb.update_warship(warship)
		self.logger.debug('Warships updated.')
	
	def update_shipparams(self):
		"""
		Update shipparameters table in database.
		"""
		self.logger.debug('Updating shipparams in database.')
		ship_ids = self.wowsdb.get_ship_ids()
		for ship_id in ship_ids:
			param = self.wowsapi.get_ship_profile(ship_id[0])
			self.wowsdb.update_shipparam(param)

		self.logger.debug('Ship parameters updated.')

	def update_modules(self):
		"""
		Update ship modules table in database.
		"""
		self.logger.debug('Updating modules in database.')
		warships = self.wowsdb.get_warships()
		pbar = tqdm(total=len(warships))
		module_list = []
		for warship in warships:
			module_ids = warship.get_module_id_list()
			for module_id in module_ids:
				temp = self.wowsdb.get_module(module_id)
				if temp:
					continue
				module = self.wowsapi.get_module(module_id)
				self.wowsdb.update_module(module)
			pbar.update()
		pbar.close()
		self.logger.debug('Modules updated.')