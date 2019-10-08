import discord
import matplotlib
from scripts.logger import Logger
from discord.ext import commands, tasks 


class Roles(commands.Cog):
	__slots__ = ('logger',)

	def __init__(self, logger=None):
		self.logger = Logger(__name__) if logger is None else logger


	@commands.group()
	async def roles(self, ctx):
		""" 役職をいじれるよ！ """
		if ctx.invoked_subcommand is None:
			await ctx.send('コマンドも教えてね！')


	@roles.command()
	async def create(self, ctx, name, color):
		""" 役職を作るよ！ roles create '役職の名前' '色（英語で教えてね！）' """
		try:
			color = matplotlib.colors.cnames.get(color)
		except IndexError:
			await ctx.send('名前と色も教えてね！')	
			return

		if color is not None:
			color = discord.Colour(int(str(color)[1:], 16))
			await ctx.guild.create_role(name=name, colour=color)
			await ctx.send(name + ', いっちょあがり！')
		else:
			await ctx.send('そんな色知らないよ！')


	@roles.command()
	async def listnotused(self, ctx):
		""" 使ってない役職の一覧を貼るよ！ """
		self.logger.debug('Processing listnotused.')
		b = False
		for role in ctx.guild.roles:
			if role.is_default():
				continue
			for member in ctx.guild.members:
				if role in member.roles:
					b = True
			if not(b):
				await ctx.send(role.name + ',\t誰も使ってないよ！')
			b = False

		await ctx.send('はい、終わり！')


	@roles.command()
	async def deletenotused(self, ctx):
		""" 使ってない役職をすべて削除するよ！ """
		self.logger.debug('Processing deletenotused.')
		b = False
		for role in ctx.guild.roles:
			if role.is_default():
				continue
			for member in ctx.guild.members:
				if role in member.roles:
					b = True

			if not(b):
				self.logger.debug('Deleting role.')
				await ctx.send(role.name + ', バーン！')
				await role.delete()
				self.logger.debug('Deleted role.')
			b = False
		self.logger.debug('Processed deletenotused.')
		await ctx.send('はい、終わり！')


	@roles.command()
	async def hoist(self, ctx):
		""" 全ての役職をオンラインメンバーとは別に役職メンバーを表示するよ！ """
		for role in ctx.guild.roles:
			if not role.hoist:
				await role.edit(hoist=True)
		await ctx.send(':thumbsup:')


	@roles.command()
	async def mentionoff(self, ctx):
		""" 全ての役職をメンション不可能にするよ！ """
		for role in ctx.guild.roles:
			if role.mentionable:
				await role.edit(mentionable=False)
		await ctx.send(':thumbsup:')