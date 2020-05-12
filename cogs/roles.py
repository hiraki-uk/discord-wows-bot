import discord
import matplotlib
from discord.ext import commands, tasks

from scripts.logger import Logger
from scripts.scripts import get_guild


class Roles(commands.Cog):
	__slots__ = ('bot', 'logger')

	def __init__(self, bot):
		self.bot = bot
		self.logger = Logger(__name__)

	@commands.group()
	async def roles(self, ctx):
		""" 役職をいじれるよ！ """
		if ctx.invoked_subcommand is None:
			await ctx.send('コマンドも教えてね！')

	@roles.command()
	async def create(self, ctx, name, color='red'):
		""" 役職を作るよ！ roles create '役職の名前' '色（英語で教えてね！）' """
		try:
			color = matplotlib.colors.cnames.get(color)
		except IndexError:
			await ctx.send('名前と色も教えてね！')	
			return

		color = discord.Colour(int(str(color)[1:], 16))
		await ctx.guild.create_role(name=name, colour=color)
		await ctx.send(name + ', いっちょあがり！')

	# @roles.command()
	# async def random(self, ctx, target=None):
	# 	if target is None:
	# 		await ctx.send('役職誰にあげるのかわかんないよ〜')
	# 		return
	# 	elif not check_user(target):
	# 		await ctx.send('誰この人！')
	# 		return
		
	# 	user = get_user(name=target)
	# 	give_role(user, role)
		
	# 	await ctx.send('じゃーん！何あげたでしょー')

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

	# @roles.command()
	# async def hoist(self, ctx):
	# 	""" 全ての役職をオンラインメンバーとは別に役職メンバーを表示するよ！ """
	# 	for role in ctx.guild.roles:
	# 		if not role.hoist:
	# 			await role.edit(hoist=True)
	# 	await ctx.send(':thumbsup:')

	@roles.command()
	async def mentionoff(self, ctx):
		""" 全ての役職をメンション不可能にするよ！ """
		for role in ctx.guild.roles:
			if role.mentionable:
				await role.edit(mentionable=False)
		await ctx.send(':thumbsup:')

	# """
	# removed roles.on_ready as duplication of 
	# methods may be not good
	# """
	# @commands.Cog.listener()
	# async def on_ready(self):
	# 	# get all members as list
	# 	members = get_guild(self.bot).members
	# 	self.logger.debug(f'{len(members)} members found.')

	# 	# add or remove game activity
	# 	for member in members:
	# 		activity = member.activities
	# 		activity_role_now = get_activity_role_now(member)

	# 		# do nothing 
	# 		if not activity and not activity_role_now:
	# 			self.logger.debug(f'no activity found for {member.nick}.')
	# 			continue
	# 		# has roles on but not playing anything
	# 		elif not activity and activity_role_now:
	# 			remove_activity_role(member)
	# 		# has roles on and playing something
	# 		elif activity and activity_role_now:
	# 			remove_activity_role(member)
	# 			give_activity_role(member)
	# 		# no roles but playing something
	# 		else:
	# 			give_activity_role(member)
			
	# 		self.logger.debug(f'activity found for {member.nick}.')

	# @commands.Cog.listener()
	# async def on_member_update(self, before, after):
	# 	"""
	# 	When member was updated, 
	# 	"""
