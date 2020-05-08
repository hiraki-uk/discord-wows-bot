import asyncio
import datetime
import json
import sqlite3
import traceback

import requests
from discord.ext import commands, tasks
from wowspy import Region, Wows
from wows.worldofwarships import WorldofWarships
from cogs.cogfunctions.database import Database
from scripts.logger import Logger

db_path = 'wows.db'


class WowsCog(commands.Cog):
	def __init__(self, bot, wows_app_id):
		self.bot = bot
		self.logger = Logger(self.__class__.__name__)
		self.wows = WorldofWarships(wows_app_id, db_path)

	