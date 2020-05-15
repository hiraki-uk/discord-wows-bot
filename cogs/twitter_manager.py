"""
twitter_manager module.
"""

import asyncio
from os import getenv

import discord
import twitter
from discord import Embed
from discord.ext import commands, tasks
from dotenv import load_dotenv

try:
	from scripts.logger import Logger
except:
	pass

load_dotenv('.env')

_wowsnewsjp_id = 1063025161014796289
_base_url = 'https://twitter.com/wowsnews_jp/status/'


class Twitter_manager(commands.Cog):
	"""
	twitter_manager class.
	Responsible for interactions with twitter.
	"""
	def __init__(self, bot):
		self.wowsnews_jp = WowsNewsJP()
		self.bot = bot
		statuses = self.wowsnews_jp.get_latest_statuses()
		self.latest_id = statuses[0].id
		self.logger = Logger(__name__)
		self.check_task.start()

	@tasks.loop(seconds=30)
	async def check_task(self):
		self.logger.debug('Checking for latest tweets.')
		statuses = self.wowsnews_jp.get_latest_statuses()
		# return if up to date
		if self.latest_id == statuses[0].id:
			self.logger.debug('Twitter_manager is up to date.')
			return
		to_send = []
		for status in statuses:
			# stop if id is the one saved
			if status.id == self.latest_id:
				self.logger.debug('This tweet has already been sent.')
				break
			to_send.insert(0, status)

		for guild in self.bot.guilds:
			for channel in guild.channels:
				if channel.name == 'wows-news':
					for status in to_send:
						await channel.send(f'{status.text}\n{_create_url(status)}')

		self.latest_id = statuses[0].id
		self.logger.debug('Finished sending.')

	@check_task.before_loop
	async def before_check(self):
		await self.bot.wait_until_ready()
		await asyncio.sleep(1)


class WowsNewsJP:
	"""
	WowsNewsJP class.
	Represents twitter account for @wowsclans_jp.
	"""
	def __init__(self):
		self.twitter_api = twitter.Api(
			consumer_key = getenv('TWITTER_CONSUMER_KEY'),
			consumer_secret = getenv('TWITTER_CONSUMER_SECRET'),
			access_token_key = getenv('TWITTER_TOKEN_KEY'),
			access_token_secret = getenv('TWITTER_TOKEN_SECRET')
		)

	def get_latest_statuses(self, count=3):
		"""
		Checks for the latest statuses of this account.
		Returns latest status first.
		"""
		statuses = self.twitter_api.GetUserTimeline(user_id=_wowsnewsjp_id, count=count)
		return statuses


def _create_url(status):
	return _base_url + status.id_str


if __name__ == '__main__':
	w = WowsNewsJP()
	print(w.get_latest_statuses())
