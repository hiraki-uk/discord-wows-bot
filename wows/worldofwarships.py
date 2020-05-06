from scripts.logger import Logger
from wows.wowsapi import Wows_API
from wows.wowsdb import Wows_database


class WorldofWarships:
	def __init__(self, key, db_path):
		self.logger = Logger(self.__class__.__name__)
		self.logger.debug('Initializing wows class.')
		self.wowsapi = Wows_API(key)
		self.wowsdb = Wows_database(db_path)

	def update_warships(self):
		"""
		Update warships table in database.
		"""
		self.logger.debug('Updating warships in database.')
		# check version
		version_db = self.wowsdb.get_db_version()
		version_api = self.wowsapi.get_api_version()
		print(version_api)
		print(version_db)
		# return if version is up to date.
		if version_db == version_api:
			self.logger.debug(f'Returning as database has latest version {version_db}.')
			return

		# update warships then update version
		warships = self.wowsapi.get_warships()
		self.wowsdb.update_warships(warships)
		self.wowsdb.update_version(version_api)

		self.logger.debug('Warships updated.')