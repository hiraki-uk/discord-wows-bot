import datetime
import os

from discord.ext import commands, tasks
from dotenv import load_dotenv
from utils.fourFn import calc as c
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
	async def eval(self, ctx, *, args):
		"""使える文字は ^,*,/,+,-,PI,E,(,),sin,cos,tan,exp,abs,trunc,round,sgn,multiply,hypot,allだよ！"""
		result = c(args)
		if not result:
			await ctx.send('はいエラー')
			return
		await ctx.send(result)

	# @commands.command(aliases=['こんさん'])
	# async def konsan(self, ctx):
	# 	""" ZEALホームページのURLだよ～ """
	# 	emoji = ctx.bot.get_emoji(794537197436403742)
	# 	if not emoji:
	# 		return
	# 	mes = f'https://twitter.com/himajin_0002/status/1345854915894120449\n\n' \
	# 	f'いい感じ!!(自社調べ)\n{str(emoji)}'
	# 	await ctx.send(mes)
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
		if not (now.hour == 3 and now.minute == 30):	
			return	
		if self.last_sent_date == now.date():	
			return	
		else:	
			self.last_sent_date = now.date()	

		for guild in self.bot.guilds:	
			for channel in guild.channels:	
				if channel.name == 'bot-room':	
					await channel.send('<@&819637690349256765> 334の時間だよ！！！！！') 