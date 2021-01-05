import io
from sqlite3.dbapi2 import Binary
import discord

from discord.ext import commands
from gameparams.api_db import ApiDB
from utils.logger import Logger

from wows.wowsapi import WowsApi

filepath = 'res/temp.jpg'


class WowsCog(commands.Cog):
	def __init__(self, bot, wows_application_id):
		self.bot = bot
		self.logger = Logger(self.__class__.__name__)
		self.db = ApiDB()
		self.api = WowsApi(wows_application_id)


	@commands.command(aliases=['param'])
	async def pm(self, ctx, *, name=None):
		"""
		そのぽふねのデータ教えてあげる！
		"""
		self.logger.info('Recieved param command.')
		if name is None:
			await ctx.send('どのぽふねのデータがほしいの？ うむらると？気合でやって')
			return
		result = self.db.get_image(name)
		if not result:
			self.logger.debug('No result found.')
			await ctx.send('誰よその女！')
			return
		# multiple matches
		elif isinstance(result, list):
			self.logger.info('Found multiple matches for a warship.')
			mes = 'いっぱいヒットしちゃったよ～' \
				'```' + ', '.join(result) + '```'
			await ctx.send(mes)
		# send image
		else:
			data = io.BytesIO(result)
			await ctx.send(file=discord.File(data, 'ship.png'))