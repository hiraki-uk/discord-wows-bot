import discord
from discord.ext import commands

from cogs.cogfunctions.honda import card_process as card_proc
from cogs.cogfunctions.honda import janken_process as janken_proc


class Shitposting(commands.Cog):
	"""	産業廃棄物処理場 """

	@commands.command()
	async def elshaddai(self, ctx):
		""" 話をしよう。あれはー """
		with open('res/elshaddai.txt', 'r', encoding='utf-8') as f:
			await ctx.send('```' + f.read() + '```')
			
	@commands.command()
	async def dokata(self, ctx):
		""" やったぜ。投稿者: 変態糞土方 """
		with open('res/dokata.txt', 'r', encoding='utf-8') as f:
			await ctx.send('```' + f.read() + '```')
			
	@commands.command()
	async def jow(self, ctx):
		""" ～JOWは懲罰する～ """
		with open('res/jow.txt', 'r', encoding='utf-8') as f:
			await ctx.send('```' + f.read() + '```')

	# janken 
	@commands.command()
	async def janken(self, ctx, choice=None):
		"""	なんで負けたか　明日まで考えといてください！ """
		choices = ('rock', 'paper', 'scissors')
		if choice not in choices:
			await ctx.send('エラー:\nただいまアクセス集中により、返信対応に時間がかかっております。\n申し訳ございませんが、しばらくお待ちください。')
			return
		await janken_proc(ctx, choice)


	# card battle
	@commands.command()
	async def card(self, ctx, choice=None):
		""" 裏の裏の裏まで！ """
		choices = ('a', 'A', 'b', 'B')
		if choice not in choices:
			await ctx.send('エラー:\nただいまアクセス集中により、返信対応に時間がかかっております。\n申し訳ございませんが、しばらくお待ちください。')
			return			
		await card_proc(ctx, choice)
