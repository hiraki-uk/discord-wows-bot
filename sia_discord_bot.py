"""
Main python file.
English description is for developers, where Japanese ones will be desplayed to users.  
"""

import asyncio
import os
import sys
from pathlib import Path

from discord import Activity, ActivityType
from discord.ext import commands, tasks
from dotenv import load_dotenv

from cogs.cogs import Cogs
from cogs.listeners import Listener
from cogs.newroles import NewRoles
from cogs.roles import Roles
from cogs.shitposting import Shitposting
from cogs.twitter_manager import Twitter_manager
from cogs.vc import VoiceChannel
from cogs.weather import Weather
from cogs.wows import WorldOfWarships
from scripts.logger import Logger
from scripts.scripts import add_cogs


def bot_setup():
	# path to environment variables
	env_path = '.env'
	load_dotenv(dotenv_path=env_path)

	# get data from .env
	prefix = os.getenv('PREFIX')
	key = os.getenv('DISCORD_BOT_KEY')
	activity_name = os.getenv('ACTIVITY_NAME')
	db_path = os.getenv('DB_PATH')
	# register activity, prefix, commands
	if activity_name is None:
		bot = commands.Bot(command_prefix=prefix)
	else:
		activity = Activity(name=activity_name, type=ActivityType.playing)
		bot = commands.Bot(command_prefix=prefix, activity=activity)
	add_cogs(bot,
			Cogs(bot),
			Roles(bot),
			Listener(bot),
			NewRoles(bot),
			Shitposting(bot),
			VoiceChannel(bot),
			Weather(bot),
			WorldOfWarships(bot, os.getenv('WOWS_APPLICATION_ID')),
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
