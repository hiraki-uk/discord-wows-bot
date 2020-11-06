from database.wows_db import Wows_database
from discord.ext import commands, tasks
from utils.logger import Logger


class WowsDb(commands.Cog):
	"""
	WowsDb cog class.
	"""
	def __init__(self, bot):
		self.bot = bot
		self.db = Wows_database('database/wows.db')
		self.latest_id = self.db.get_latest_id()
		self.logger = Logger(self.__class__.__name__)
		self.db_task.start()


	@commands.command()
	async def dbcheck(self, ctx, _id=None):
		if not _id:
			await ctx.send(f'Using latest id {self.latest_id}.')
			_id = self.latest_id
		try:
			_id = int(_id)
		except:
			await ctx.send('Cannot parce into an integer.')
			return
		if self.latest_id < _id:
			await ctx.send('id greater than latest id.')
			return
		data = self.db.get_news(_id)
		# send news
		for guild in self.bot.guilds:
			for channel in guild.channels:
				if channel.name == 'debug':
					mes = data.title + '\n' + data.description
					await channel.send(mes)


	@tasks.loop(seconds=50)
	async def db_task(self):
		print('Starting db_task.')
		res = self.db.get_latest_id()
		# if new news found
		if not res:
			return
		latest_id = res
		if latest_id != self.latest_id:
			for i in range(latest_id - self.latest_id):
				data = self.db.get_news(self.latest_id)

				# send news
				for guild in self.bot.guilds:
					for channel in guild.channels:
						if channel.name == 'debug':
							mes = data.title + '\n' + data.description
							await channel.send(mes)
				self.latest_id += 1