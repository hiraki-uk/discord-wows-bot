import asyncio
import datetime
import json
import sqlite3
import traceback

import requests
from discord.ext import commands, tasks
from wowspy import Region, Wows

from cogs.cogfunctions.database import Database
from scripts.logger import Logger

db_path = 'players.db'


class WorldOfWarships(commands.Cog):
	def __init__(self, bot, wows_app_id):
		self.bot = bot
		self.wowsmanager = WowsdbManager()
		self.wowsapi = WowsAPI(wows_app_id)
		self.logger = Logger(self.__class__.__name__)

	@commands.command()
	async def register(self, ctx, ign=None):
		""" あなたを登録するよ！ """
		self.logger.debug('Checking credentials before registering.')
		if ign is None:
			await ctx.send('いんげーむねーむも教えてね！')
			return
		await ctx.send(f'{ign}さんね、ちょっと待ってて')			
		discord_id = ctx.message.author.id
		player_data = self.wowsapi.create_player_info(ign)
		if player_data is None:
			await ctx.send('ごめんえらったあとででもっかいやってみて！')
			return
		self.logger.debug('Passing data to manager class.')
		self.wowsmanager.register(player_data, discord_id)

		await ctx.send(':thumbsup:')

	@commands.command()
	async def stats(self, ctx, name=None):
		if name is None:
			await ctx.send('どの船の情報が欲しいの？')

	@commands.command()
	async def deregister(self, ctx):
		""" あなたの登録を解除するよ！ """
		discord_id = ctx.message.author.id	
		self.wowsmanager.deregister(discord_id)
		await ctx.send(':thumbsup:')

	@commands.command()
	async def update(self, ctx):
		"""
		Create and update info based on data in database.
		"""
		self.wowsmanager.update()

	@commands.command()
	async def update_task(self, ctx):
		pass


class WowsAPI(Wows):
	def __init__(self, key):
		self.logger = Logger(self.__class__.__name__)

	def create_player_info(self, player_name):
		self.logger.debug(f'Creating player info for {player_name}.')
		player = self.players(Region.AS, player_name)
		if not player:
			return
		elif player['status'] != 'ok':
			return
		player_id = player['data'][0]['account_id']
		player_data = self.player_personal_data(Region.AS, player_id)
		if not player_data:
			return
		elif player_data['status'] != 'ok':
			return
		player_data = player_data['data'][str(player_id)]
		self.logger.debug('Created player_data successfully.')
		return player_data

	def create_ship_info(self, ship_name):
		self.logger.debug(f'Creating ship_info for {ship_name}.')
		ship = self.ship_parameters(Region.AS, )


class WowsdbManager:
	"""
	WowsdbManager class.
	Responsible for interaction between wows and database.
	"""
	def __init__(self):
		self.database = Wows_database(db_path)
		self.logger = Logger(self.__class__.__name__)

	def register(self, player, discord_id):
		self.logger.debug('Checking credentials.')
		if self.database.is_registered(discord_id):
			self.logger.debug('User already registered.')
			return
		self.logger.debug('Registering player into database.')
		self.database.register(player, discord_id)

	def deregister(self, discord_id):
		self.logger.debug('Checking credentials.')
		if not self.database.is_registered(discord_id):
			return
		self.logger.debug('Deregistering user.')
		self.database.deregister(discord_id)


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
		""")
		self.logger.debug('Created wows database table.')

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

if __name__ == '__main__':
	wows = Wows('6e513bc6bf277c5bf46d03d7b11dbe68')
	with open('temp.json', 'w') as f:
		f.write(wows.warships(region=Region.AS, language='ja'))