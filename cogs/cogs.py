import datetime
import os
import random

from discord.ext import commands, tasks
from dotenv import load_dotenv
from utils.logger import Logger

tz = datetime.timezone(datetime.timedelta(hours=9))

load_dotenv(dotenv_path='.env')
ver = os.getenv('VERSION')


class Cogs(commands.Cog):
	__slots__ = ('bot', 'logger')
	
	"""	基本的な命令をここに格納してるよ！ """
	def __init__(self, bot):
		self.bot = bot
		self.logger = Logger(self.__class__.__name__)
		self.last_sent_date = None
		self.hanshin_task.start()

	# version
	@commands.command()
	async def version(self, ctx):
		""" 現在バージョンを教えるよ！ """
		await ctx.send(ver)

	# delete ten messages
	@commands.command()
	async def delten(self, ctx):
		""" 直近10メッセージを削除するよ！ """
		async for message in ctx.channel.history(limit=11):
			await message.delete()

	# delete five messages
	@commands.command()
	async def delfive(self, ctx):
		""" 直近5メッセージを削除するよ！ """
		async for message in ctx.channel.history(limit=6):
			await message.delete()

	# # server status
	# @commands.command()
	# async def vmstat(self, ctx):
	# 	""" みつばサーバーの負荷状況を教えるよ！ """
	# 	stats = exec('vmstat')
	# 	await ctx.send('``` \
	# 		stats \
	# 	````')
		
	# urls
	@commands.command()
	async def jyantama(self, ctx):
		""" じゃんたまのURLだよ～ """
		mes = ':thumbsup:\nhttps://game.mahjongsoul.com/'
		await ctx.send(mes)
	@commands.command()
	async def numbers(self, ctx):
		""" statsのURLだよ～ """
		mes = ':thumbsup:\nhttps://asia.wows-numbers.com/'
		await ctx.send(mes)
	@commands.command()
	async def hp(self, ctx):
		""" wowsホームページのURLだよ～"""
		mes = ':thumbsup:\nhttps://worldofwarships.asia/'
		await ctx.send(mes)
	@commands.command()
	async def zeal(self, ctx):
		""" ZEALホームページのURLだよ～ """
		mes = ':thumbsup:\nhttps://zeal.live-on.net'
		await ctx.send(mes)

	# @commands.command()
	# async def slot(self, ctx):
	# 	""" ランク戦味方占い！"""
	# 	with open('res/rank_prefix.txt', 'r') as f:
	# 		prefix = f.read()
	# 	indexes = random.random(len(prefix), 6) # index of your teammates
	# 	prefixes = [prefix[i] for i in range(indexes)]
	# 	ships = []
	# 	sol = [prefix[i] + ships[i] for i in range(indexes)]

	# 	await ctx.send('\n'.join(sol))


	@tasks.loop(seconds=50)
	async def hanshin_task(self):
		print('Starting hanshin task.')
		now = datetime.datetime.now(tz=tz)
		print(now)
		if not (now.hour == 3 and now.minute == 30):
			return
		if self.last_sent_date == now.date():
			return
		else:
			self.last_sent_date = now.date()
			
		for guild in self.bot.guilds:
			for channel in guild.channels:
				if channel.name == 'main':
					await channel.send('334の時間です！！！！！')