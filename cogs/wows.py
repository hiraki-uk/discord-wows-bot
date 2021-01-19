import io

import discord
from discord.ext import commands
from utils.database import Database
from utils.logger import Logger


class WowsCog(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
		self.logger = Logger(self.__class__.__name__)
		self.db = ImgDB()


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
			try:
				data = io.BytesIO(result)
				await ctx.send(file=discord.File(data, 'ship.png'))
			except:
				await ctx.send('めっちゃ変なエラーでたごめんしあに伝えて～ｗ')


class ImgDB:
	def __init__(self):
		self.db = Database('res/id_api.db')


	def get_image(self, name):
		"""
		Get image.
		"""
		result = self.db.fetchall(f'SELECT name FROM ships WHERE name like ?', (f'%{name}%',))
		results = list(map(lambda x: x[0], result))
		# if one hit, return it
		if len(results) == 1:
			img = self.get_image_fin(results[0])
			return img
		else:
			names = [n for n in results if
				not n.startswith('[') and
				not n.endswith(' B') and
				not n.startswith('ARP ')]
			# if exact match
			if len(names) == 1:
				img = self.get_image_fin(names[0])
				return img
			for n in names:
				if n.lower() == name.lower():
					img = self.get_image_fin(n)
					return img
			return names

			
	def get_image_fin(self, name):
		result = self.db.fetchone('SELECT img_final FROM ships WHERE name=?', (name,))
		if len(result) == 1:
			return result[0]


