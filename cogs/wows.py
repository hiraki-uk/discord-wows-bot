from discord.ext import tasks, commands
from enum import Enum
from wowspy import Wows 


db_path = 'players.db'


class WorldOfWarships(commands.Cog):
	def __init__(self):
		pass

	@commands.command()
	async def register(self, ctx, name):
		""" あなたを登録するよ！ """
		await ctx.send(f'{name}さんね、ちょっと待ってて')			
		# get player id from Wows
		

	@commands.command()
	async def deregister(self, ctx):
		pass
	
	@commands.command()
	async def update(self, ctx):
		pass

	@commands.command()
	async def update_task(self, ctx):
		pass


class WowsDatabase:
	def __init__(self, db_path):
		self.database = Database(db_path)
		self.logger = Logger(__name__)
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
		CREATE TABLE wowsnews(
			id INTEGER PRIMARY KEY,
			name TEXT,
			clan TEXT
		);
		""")
		self.logger.debug('Created wows database table.')


	def register(self, name):
		cmd = 'INSERT INTO players'
		self.db.execute('')


	def update(self, name_before, name_after):
		pass

	def deregister(self, name):
		pass


import asyncio
import datetime
import sqlite3
import traceback

import requests

from database.database import Database
from database.scrape_facebook import get_facebook_articles
from database.scrape_medium import get_medium_articles
from database.scrape_wowshp import get_hp_articles
from scripts.Exceptions import ScrapingException
from scripts.logger import Logger


class Wows_database:
	"""
	Scrapes and registers data into database.
	"""
	__slots__ = ('database', 'logger')

	def __init__(self, db_path):
		self.database = Database(db_path)
		self.logger = Logger(__name__)
		# if db file not found or empty, create file
		try:
			with open(db_path, 'rb') as f:
				if f.read() == b'':
					self._create_table()
		except Exception as e:
			self.logger.info('Database not found.')
			self._create_table()


	async def update(self):
		"""
		Update database.
		"""
		self.logger.info('Update started.')
		try:
			await self._update_hp()
		except Exception:
			self.logger.critical(f'Exception while updating: {traceback.format_exc()}')
		self.logger.info('Update finished.')


	def _create_table(self):
		self.logger.debug('Creating wows database table.')
		self.database.executescript("""
		CREATE TABLE wowsnews(
			id INTEGER PRIMARY KEY AUTOINCREMENT,
			source TEXT,
			title TEXT,
			description TEXT,
			url TEXT,
			img TEXT
		);
		""")
		self.logger.debug('Created wows database table.')


	def _get_latest(self, source:str):
		"""
		Get latest news stored in database.

		Returns
		-------
		res : tuple, None
		"""
		self.logger.debug(f'Starting _get_latest source: {source}')
		res = self.database.fetchone('SELECT * FROM wowsnews WHERE source==? ORDER BY id DESC', (source,))
		self.logger.debug(f'_get_latest result: {res}')
		
		return res


	async def _update_medium(self):
		"""
		Check for new articles, if found update db.
		"""
		self.logger.info('Updating medium.')
		try:
			data = get_medium_articles()
		except ScrapingException:
			self.logger.critical('Scraping failed.')
			return

		# get latest data in database
		data_db = self._get_latest('medium')
		# if up to date, return
		if _is_same_data(data_db, data[0]):
			self.logger.info('Medium is up to date.')
			return
		# counter shows how many articles to update
		counter = 0
		for d in data:
			# if url is most recent in db
			if d == data_db:
				break
			counter += 1
		# data.reverse() not working, so using temp reverse()
		temp = data
		temp.reverse()
		news = temp[:counter]
		try:
			for new in news:
				self.database.execute('INSERT INTO wowsnews(source, title, description, url, img) VALUES(?, ?, ?, ?, ?)', new)
		except Exception as e:
			self.logger.critical(f'Inserting into database failed: {e}')
			return
		self.logger.info('Updated medium.')


	def _url_exists(self, url:str):
		self.logger.debug('Checking if url already exists in database.')
		self.logger.debug(f'url is {url[10:]}')
		try:
			res = self.database.fetchone(f'SELECT * FROM wowsnews WHERE url==?', (url,))
		except Exception as e:
			self.logger.critical(f'Fetching datbase failed: {e}')
			res = None
		self.logger.debug(f'Result: {res}')
		if not res:
			return False
		return True

	
def _is_same_data(data_from_db:tuple, data:tuple):
	"""
	Returns true if two data are the same excluding the id.
	Else returns false.
	"""
	if data_from_db == None:
		return False
	temp = tuple(data_from_db[1:])
	if temp != data:
		return False
	return True


def _has_same_url(data_from_db:tuple, data:tuple):
	"""
	Returns true if two data share the same url.
	Else returns false.

	This method is craeted for comparing facebook data as
	_is_same_data return false for same article where
	pic url are different.
	"""
	if data_from_db == None:
		return False
	temp = tuple(data_from_db[1:])
	if temp[3] != data[3]:
		return False
	return True


class Region(Enum):
	ASIA = 'ASIA'
