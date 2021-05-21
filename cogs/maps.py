import io

import discord
from discord.ext import commands
from init.maps.map_db import MapDB
from utils.logger import Logger


class MapsCog(commands.Cog):
	def __init__(self, bot) -> None:
		self.bot = bot
		self.logger = Logger(self.__class__.__name__)
		self.db = MapDB()

	@commands.command()
	async def map(self, ctx, *, name=None):
		"""
		地図見たいの？いいよ！
		"""
		self.logger.info('Recieved map command.')
		if name is None:
			await ctx.send('どの地図がほしいの？')
			return
		result = self.db.get_image(name)
		if not result:
			self.logger.debug('No result found.')
			await ctx.send('ヒットなし！')
			return
		# multiple matches
		elif isinstance(result, list):
			self.logger.info('Found multiple matches.')
			mes = 'いっぱいヒットしちゃったよ～' \
				'```' + ', '.join(result) + '```'
			await ctx.send(mes)
		# send image
		else:
			try:
				data = io.BytesIO(result)
				await ctx.send(file=discord.File(data, 'map.png'))
			except:
				await ctx.send('めっちゃ変なエラーでたごめんしあに伝えて～ｗ')
