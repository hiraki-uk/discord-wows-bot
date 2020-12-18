import json

import discord
# import matplotlib
from discord.ext import commands, tasks
from utils.logger import Logger


class Roles(commands.Cog):
	__slots__ = ('bot', 'logger')

	def __init__(self, bot):
		self.bot = bot
		self.logger = Logger(self.__class__.__name__)


	@commands.group()
	async def roles(self, ctx):
		""" 役職をいじれるよ！ """
		if ctx.invoked_subcommand is None:
			await ctx.send('コマンドも教えてね！')


	# @roles.command()
	# async def create(self, ctx, name, color='red'):
	# 	""" 役職を作るよ！ roles create '役職の名前' '色（英語で教えてね！）' """
	# 	try:
	# 		color = matplotlib.colors.cnames.get(color)
	# 	except IndexError:
	# 		await ctx.send('名前と色も教えてね！')	
	# 		return

	# 	color = discord.Colour(int(str(color)[1:], 16))
	# 	await ctx.guild.create_role(name=name, colour=color)
	# 	await ctx.send(name + ', いっちょあがり！')


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
	async def countnotused(self, ctx):
		""" 使ってない役職の個数を教えるよ！ """
		self.logger.debug('Processing countnotused.')
		count = 0
		b = False
		for role in ctx.guild.roles:
			if role.is_default():
				continue
			for member in ctx.guild.members:
				if role in member.roles:
					b = True
			if not(b):
				count += 1
			b = False

		await ctx.send(f'{count}個使われてないのあったよ～！')

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
	async def mentionoff(self, ctx):
		""" 全ての役職をメンション不可能にするよ！ """
		for role in ctx.guild.roles:
			if role.mentionable:
				await role.edit(mentionable=False)
		await ctx.send(':thumbsup:')


	@tasks.loop(minutes=3)
	async def update_ranks(self):
		with open('members.json', 'r') as f:
			temp = f.read()
			if not temp:
				return
		members = json.loads(temp)

		for member in members:
			discord_id = member['discord_id']
			user = self.bot.get_member(discord_id)
			roles = user.roles
			temp = roles.sorted(key=lambda role:role.position)
			for role in temp:
				role_pos = role.id
				pass