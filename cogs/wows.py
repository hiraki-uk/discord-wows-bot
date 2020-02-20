import asyncio
import datetime
import sqlite3
import traceback
from enum import Enum

import requests
from discord.ext import commands, tasks
from wowspy import Wows

from scripts.logger import Logger

db_path = 'players.db'


class WorldOfWarships(commands.Cog):
	def __init__(self):
		self.wowsmanager = WowsdbManager()
		self.wowsapi = WowsAPI()


	@commands.command()
	async def register(self, ctx, ign=None):
		""" あなたを登録するよ！ """
		if ign is None:
			await ctx.send('いんげーむねーむも教えてね！')
			return
		await ctx.send(f'{ign}さんね、ちょっと待ってて')			
		# get wows_id from Wows
		discord_id = ctx.user.id
		player = WowsAPI.create_player_info(ign, discord_id)
		if player is None:
			await ctx.send('このぷれいやーいないみたいだよ？')
			return
		
		self.wowsmanager.register(player)


	@commands.command()
	async def deregister(self, ctx):
		pass
	
	@commands.command()
	async def update(self, ctx):
		pass

	@commands.command()
	async def update_task(self, ctx):
		pass


class WowsAPI(Wows):
	pass


class WowsdbManager:
	"""
	WowsdbManager class.
	Responsible for interaction between wows and database.
	"""
	def __init__(self):
		self.database = Wows_database(db_path)
		self.logger = Logger(__name__)


	def register(self, player):
		if self.database.is_registered(player.discord_id):
			return

		self.database.register(player)

	def update(self, name_before, name_after):
		pass

	def deregister(self, name):
		pass


class Wows_database:
	"""
	Wows_database class.
	Responsible for interactions with database.
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


	def _create_table(self):
		self.logger.debug('Creating wows database table.')
		self.database.executescript("""
		CREATE TABLE players(
			discord_id INTEGER PRIMARY KEY AUTOINCREMENT,
			wows_id INTEGER,
			in_game_name TEXT,
			clan TEXT
		);
		""")
		self.logger.debug('Created wows database table.')


	def register(self, discord_id, wows_id, in_game_name, clan):
		"""
		Register discord user into database.
		"""
		self.logger.debug(f'Registering {in_game_name}.')
		self.database.execute('INSERT INTO players VALUES()', (discord_id, wows_id, in_game_name, clan))
		self.logger.debug('Registered player.')

	
	def deregister(self, discord_id):
		"""
		Deregister discord user from database.
		"""
		self.logger.debug('Deregistering user.')
		self.database.execute('')
		self.logger.debug('Deregistered user.')
	

	def is_registered(self, discord_id):
		"""
		Checks is given discord_id is registered.
		"""
		result = self.database.fetchone('SELECT discord_id from players WHERE discord_id = ?', (discord_id,))
		return result is None


class Player:
	def __init__(self, discord_id, wows_id, in_game_name, clan):
			self.discord_id = discord_id
			self.wows_id = wows_id
			self.ign = in_game_name
			self.clan = clan