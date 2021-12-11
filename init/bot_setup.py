import discord
from config.config import get_config
from discord import Activity, ActivityType
from discord.ext import commands


class Mitsuba:
	def __init__(self):
		self.config = get_config()
		bot = bot_setup(self.config)
		self.bot = bot


def bot_setup(config):
	# register activity, prefix, commands, intents
	intents = discord.Intents.default()
	intents.presences = True
	intents.members = True

	if config['activity_name'] is None:
		bot = commands.Bot(command_prefix=config['prefix'], intents=intents)
	else:
		activity = Activity(name=config['activity_name'], type=ActivityType.playing)
		bot = commands.Bot(command_prefix=config['prefix'], activity=activity, intents=intents)
	return bot
