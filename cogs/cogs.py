import os

import discord
from discord.ext import commands, tasks
from dotenv import load_dotenv

from scripts.logger import Logger

load_dotenv(dotenv_path='.env')

ver = os.getenv('VERSION')


class Cogs(commands.Cog):
	__slots__ = ('bot', 'logger')
	
	"""	基本的な命令をここに格納してるよ！ """
	def __init__(self, bot, logger=None):
		self.bot = bot
		self.logger = Logger(__name__) if logger is None else logger

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
	
	@commands.command()
	async def test(self, ctx):
		for member in ctx.guild.members:
			print(member.activities)
