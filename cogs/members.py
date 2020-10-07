from discord.ext import commands, tasks

from scripts.logger import Logger
from wows.warship import Warship
from wows.worldofwarships import WorldOfWarships
from wows.wowsapi import WowsApi
from scripts.scripts import register, is_registered, update_members, registered_members


class Members(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
		self.logger = Logger(__name__)

	@commands.command()
	async def reg(self, ctx, discord_id=None, **kwargs):
		"""
		あなたのコト、管理してあげる♡
		"""
		self.logger.info('Starting WowsCog.reg command.')
		# get discord id
		if discord_id:
			try:
				discord_id = int(discord_id)
			except:
				await ctx.send('discord ID数字にできなかったぽい？')
				return
			user = self.bot.get_user(discord_id)
			if not user:
				await ctx.send('権限確認してないんだから変なことはやめてよね！')
				return
		else:
			discord_id = ctx.message.author.id

		# register user
		update(discord_id, kwargs)
		await ctx.send('毎度ありがとうございます♡')

	# @tasks.loop(minutes=5)
	# async def update_task(self, ctx):
	# 	""" Update members.json file. """
	# 	members_old = registered_members()
	# 	members_new = []
	# 	for member in members_old:
	# 		account_id = member['account_id']
	# 		in_game_name = self.api.get_in_game_name(account_id)
	# 		clan = self.api.get_player_clan_tag(account_id)
	# 		rank = self.api.get_rank(account_id, member['season_id'])
	# 		# use old info if none
	# 		if not in_game_name:
	# 			in_game_name = member['in_game_name']
	# 		elif not clan:
	# 			clan = member['clan']
	# 		elif not rank:
	# 			rank  = member['rank']
			
	# 		member_new = {
	# 			'discord_id': member['discord_id'],
	# 			'account_id': member['account_id'],
	# 			'in_game_name': in_game_name,
	# 			'clan': clan,
	# 			'rank': rank,
	# 			'season_id': member['season_id']
	# 		}
	# 		members_new.append(member_new)
	# 	# update file
	# 	update_members(members_new)