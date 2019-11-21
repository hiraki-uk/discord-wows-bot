import discord
from discord.ext import commands, tasks


class TwitterCogs(commands.Cog):
	""" Responsible for twitter related cogs. """
	def __init__(self, bot):
		self.bot = bot
		self.latest_news_id = 0

	
	@tasks.loop(seconds=30)
	async def news_task(self):
		"""
		Start checking latest tweets on @wowsnews_jp.
		If any found, send them to news channel.
		"""
		tweets = _get_latest_tweets(3)  
		latest_id = tweets[0].latest_id

		# initialization
		if self.latest_news_id == 0:
			self.latest_news_id = latest_id
			return
		# return if up to date
		elif self.latest_news_id == latest_id:
			return

		updates = latest_id - self.latest_news_id

		tweets.reverse()
		for i in range(updates):
			await _send(tweets[i])



		


	