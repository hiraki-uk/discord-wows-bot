import asyncio
import datetime
import gc
import traceback

from database.wows_db import Wows_database
from scripts.logger import Logger

# import objgraph



class Database_manager:
	"""
	Database manager. Responsible for running database.
	Checks for new data and stores them if any are updated.
	"""
	__slots__ = ('logger', 'wowsdb')

	def __init__(self, db_path):
		self.logger = Logger(__name__)
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
