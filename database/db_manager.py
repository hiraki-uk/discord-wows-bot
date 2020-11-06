import asyncio
import traceback

from utils.logger import Logger

from database.wows_db import Wows_database


class Database_manager:
	"""
	Database manager. Responsible for running database.
	Checks for new data and stores them if any are updated.
	"""
	__slots__ = ('logger', 'wowsdb')

	def __init__(self, db_path):
		self.logger = Logger(self.__class__.__name__)
		self.wowsdb = Wows_database(db_path)


	async def start(self):
		"""
		Start updating database.
		"""
		while 1:
			# update wows

			try:
				self.logger.info('Starting wows database update.')
				await self.wowsdb.update()
				self.logger.info('Finished wows database update.')
			except Exception as e:
				self.logger.critical(traceback.format_exc())
				
			await asyncio.sleep(60*3)
