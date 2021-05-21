"""
Main python file.
English description is for developers, where Japanese ones will be desplayed to users.  
"""
import asyncio
import os

import discord
from discord import Activity, ActivityType
from discord.ext import commands
from dotenv import load_dotenv

from cogs.cogs import Cogs
from cogs.listeners import Listener
from cogs.maps import MapsCog
# from cogs.membersCog import MembersCog
from cogs.roles import Roles
from cogs.shitposting import Shitposting
# from cogs.twitter_manager import Twitter_manager
from cogs.vc import VoiceChannel
from cogs.weather import Weather
from cogs.wows import WowsCog
# from cogs.wows_db import WowsDb
from utils.scripts import add_cogs


def bot_setup():
	# path to environment variables
	env_path = '.env'
	load_dotenv(dotenv_path=env_path)

	# get data from .env
	prefix = os.getenv('PREFIX')
	key = os.getenv('DISCORD_BOT_KEY')
	activity_name = os.getenv('ACTIVITY_NAME')
	db_path = os.getenv('DB_PATH')
	wows_application_id = os.getenv('WOWS_APPLICATION_ID')

	# register activity, prefix, commands, intents
	intents = discord.Intents.default()
	intents.presences = True
	intents.members = True

	if activity_name is None:
		bot = commands.Bot(command_prefix=prefix, intents=intents)
	else:
		activity = Activity(name=activity_name, type=ActivityType.playing)
		bot = commands.Bot(command_prefix=prefix, activity=activity, intents=intents)
	add_cogs(bot,
			Cogs(bot),
			Roles(bot),
			Listener(bot),
			MapsCog(bot),
			# MembersCog(bot, wows_application_id),
			Shitposting(bot),
			VoiceChannel(bot),
			Weather(bot),
			WowsCog(bot),
			# WowsDb(bot),
			# Twitter_manager(bot),
	)
	return bot, key


if __name__ == '__main__':
	bot, key = bot_setup()

	loop = asyncio.get_event_loop()
	try:
		loop.run_until_complete(
				bot.start(key)
		)
	except KeyboardInterrupt:
		loop.run_until_complete(bot.logout())
	finally:
		loop.close()
