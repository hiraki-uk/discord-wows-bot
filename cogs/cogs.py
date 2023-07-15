import datetime
from random import random

import requests
from discord.ext import commands, tasks

from init.bot_setup import Mitsuba
from utils.fourFn import calc
from utils.logger import Logger

tz = datetime.timezone(datetime.timedelta(hours=9))


class Cogs(commands.Cog):
	__slots__ = ('mitsuba', 'logger', 'last_sent_date')


	"""	基本的な命令をここに格納してるよ！ """
	def __init__(self, mitsuba: Mitsuba):
		self.mitsuba = mitsuba
		self.logger = Logger(self.__class__.__name__)
		self.last_sent_date = None


	# version
	@commands.command()
	async def version(self, ctx):
		""" 現在バージョンを教えるよ！ """
		await ctx.send(self.mitsuba.config.get('version'))


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
		mes = ':thumbsup:\nhttps://zeal-corporation.sakura.ne.jp'
		await ctx.send(mes)


	# calculations
	@commands.command()
	async def eval(self, ctx, *, args=None):
		""" ^,*,/,+,-,PI,E,(,),sin,cos,tan,exp,abs,trunc,round,sgn,multiply,hypot,all使えるよ！"""
		if args is None:
			await ctx.send('ゼロ！うるせえかえれ！')
			return
		result = calc(args)
		if result is None:
			await ctx.send('はいエラー')
			return
		await ctx.send(result)


	@commands.command(aliases=['こんさん'])
	async def konsan(self, ctx):
		""" こんさん！？！？！？ """
		emoji = ctx.bot.get_emoji(794537197436403742)
		if not emoji:
			return
		mes = f'いい感じ!!(自社調べ)\n{str(emoji)}'
		await ctx.send(mes)

	@commands.command()
	async def minecraft(self, ctx):
		""" マイクラサーバーのIPを教えるよ！ """
		res = requests.get('https://ifconfig.me')
		await ctx.send(f'はい！\r\n{res.text}:1919')

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
