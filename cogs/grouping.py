import random

import discord
from discord.ext import commands, tasks


class Grouping(commands.Cog):
	"""
	Grouping class for grouping people.
	"""
	def __init__(self):
		pass

	@commands.command()
	async def newgrpup(self, ctx, group_str='2'):
		try:
			group = int(group_str)
		except:
			await ctx.send('これ数字じゃないよわかんないよ～')
			return
		
		await ctx.send('ぶんぼ！挙手！終わったら〆てね！')
		users = [user1, user2]
		#  after 〆
		if len(users) < group:
			await ctx.send(f'{group}グループも作れないよ～やり直して～')
			return
		await ctx.send('')

		message = ''

	@commands.command()
	async def group(self, ctx, groups_str=None, players_str=None):
		if groups_str is None or players_str is None:
			message = 'どうやってチーム分けするか教えてね！\n' \
			'例えば```3,3,2```人チームで```A,B,C,D,E,F,G,H```が参加者だとしたら\n' \
			'```group 3,3,2 A,B,C,D,E,F,G,H```って書いてね！空白変なとこあるとバグるよ～'
			await ctx.send(message)
			return
		# check validity of number of players
		groups = groups_str.split(',')
		players = players_str.split(',')
		if sum(map(lambda x:int(x), groups)) != len(players):
			await ctx.send('人数おかしくない？ｗ算数ちゃんとして？ｗ')
			return
		random.shuffle(players)
		message = 'グループ分けはっぴょー！:tada:\n'
		group_no = 0
		for i in range(len(groups)):
			message += f'グループ{group_no+1}\n```' 
			for j in range(int(groups[group_no])):
				message += players.pop()
			message += '```\n'
			group_no += 1
		await ctx.send(message)
