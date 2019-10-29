import asyncio
import sqlite3

import discord
from discord import Embed
from discord.ext import commands, tasks
from cogs.cogfunctions.database import Database
try:
	from scripts.logger import Logger
except:
	from logging import Logger


class Botdb_checker(commands.Cog):
	""" Handles the interaction between you and db. """
	__slots__ = ('logger', 'database')
	def __init__(self, db_path):
		self.logger = Logger(__name__)
		self.database = Database(db_path)

	
	# send latest_id
	@commands.command()
	async def db(self, ctx, numbers=10):
		""" temporary command for smooth interactions with database. """
		if not isinstance(numbers, int):
			await ctx.send(f'tell me how many to show!')
			return
		elif not 0 < numbers and not numbers < 51:
			await ctx.send(f'give me a number from 1 to 50!')
			return
		
		res = self.database.fetchone('SELECT id FROM wowsnews ORDER BY id DESC')
		latestid = res[0]

		for i in range(latestid - numbers + 1, latestid + 1):
			res = self.database.fetchone('SELECT * FROM wowsnews WHERE id == ?', (i,))
			await ctx.send(_create_text(res))


def _create_text(res):
	"""
	create nice looking text from res in database.
	"""
	if not res:
		return ''
	return '```json\n' \
		f'latest id : {res[0]}\n' \
		f'source : "{res[1]}"\n' \
		f'title : "{res[2]}"\n' \
		f'description : "{res[3]}"\n' \
		f'url : "{res[4]}"\n' \
		f'img : "{res[5]}"' \
		'```'


class Botdb_manager(commands.Cog):
	"""	Manages bot related db. """
	__slots__ = ('bot', 'logger', 'database', 'latest_id')
	def __init__(self, bot, db_path):
		self.bot = bot
		self.logger = Logger(__name__)
		self.database = Database(db_path)
		self.database_task.start()
		self.latest_id = 0


	# send latest_id
	@commands.command()
	async def latestid(self, ctx):
		""" temporary command for smooth interactions with database. """
		await ctx.send(f'latest id is {self.latest_id}')
	

	@tasks.loop(seconds=60)
	async def database_task(self):
		"""
		Start checking the database.
		If new data found, send via discord.
		"""
		# get latest id in database
		try:
			res = self.database.fetchone('SELECT id FROM wowsnews ORDER BY id DESC')
		except Exception as e:
			self.logger.critical(e)
			res = None
		if res is None:
			self.logger.debug(f'No data found.')
			return
		latest_id_db = res[0]

		self.logger.debug(f'Latest id in database is {latest_id_db}.')
		# if result is None return
		if latest_id_db is None:
			self.logger.debug(f'No data found.')
			return
		# if self.latest_id is 0, update to latest_id_db and return
		elif self.latest_id is 0:
			self.logger.debug(f'Initializing latest id.')
			self.latest_id = latest_id_db
			return
		# if self.latest_id is same with latest_id_db return
		elif self.latest_id is latest_id_db:
			self.logger.debug('Data up to date.')
			return
		# else, send posts
		else:
			self.logger.debug('Sending posts.')
			# debug channel is 618...
			# channel = self.bot.get_channel(618259750546702336)
			channel = self.bot.get_channel(485841872347070484)
			for i in range(self.latest_id + 1, latest_id_db + 1):
				self.logger.debug(f'i is {i}, id is {self.latest_id}, latest_id_db is {latest_id_db}')
				embed = self._get_embed(i)
				self.logger.debug('Created embed')
				if embed is None:
					continue
				await channel.send(embed=embed)
			self.latest_id = latest_id_db


	@database_task.before_loop
	async def before_database_task(self):
		await self.bot.wait_until_ready()
		await asyncio.sleep(1)


	def _get_embed(self, id:int):
		"""
		Return embed of data stored in database with its id. 
		"""
		self.logger.debug('starting get embed')

		try:
			res = self.database.fetchone(f'SELECT * FROM wowsnews WHERE id=={id}')
		except Exception as e:
			self.logger.critical(e)
			res = None
		self.logger.debug(f'result: {res}')
		if res is None:
			self.logger.debug('No result found.')
			return None
		
		source = res[1]
		title = res[2]
		description = res[3]
		img = res[5]
		url = res[4]

		# create embed
		embed = Embed(title=f'Latest news on {source}!', colour=_get_color(source))

		a = embed.add_field

		if title and description:
			a(name=title, value=description)
		elif title and not description:
			a(name=title, value=title)
		elif not title and description:
			a(name=description, value=description)
		else:
			self.logger.critical(f'No title nor description for {res}')
			return None

		if img:
			embed.set_image(url=img)
		if url:
			a(name='read more here:', value=url)

		del a
		self.logger.debug('returning embed')
		return embed


def _get_color(source:str):
	if source == 'facebook':
		return 0x3b5998
	elif source == 'medium':
		return 0xffffff
	elif source == 'wowshomepage':
		return 0x0b344d