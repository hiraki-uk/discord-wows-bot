import datetime

import requests
from bs4 import BeautifulSoup
from discord import Embed
from discord.ext import commands, tasks
from utils.logger import Logger

tz = datetime.timezone(datetime.timedelta(hours=9))


class Scrape_weather:
	def __init__(self):
		pass


	def raw_tenki_data(self):
		res = requests.get('https://weather.yahoo.co.jp/weather/')
		soup = BeautifulSoup(res.text, 'html.parser')
		tenkidata = soup.find('div', {'id':'map'}).findNext('ul')
		strings = soup.find('p', {'class':'text'}).strings
		comment = ''
		for string in strings:
			comment += string
		return tenkidata, comment


	def tenki_data(self):
		td, c = self.raw_tenki_data()
		raw_tenkilist = []
		for data in td:
			# get rid of unwanted space results
			if (data == ' '): continue
			raw_tenkilist.append(data)
		return raw_tenkilist, c


	def tenki_list(self):
		tl, c = self.tenki_data()
		tenkilist = []
		for tenki in tl:
			if tenki.dt.string in ['釧路', '金沢', '鹿児島', '那覇']:
				continue
			tmp = {}
			tmp['city'] = tenki.dt.string
			tmp['climate'] = tenki.img['alt']
			tmp['temp'] = {
				'high':tenki.find('em', {'class':'high'}).string,
				'low':tenki.find('em', {'class':'low'}).string
			}
			tmp['precipitation'] = tenki.find('p', {'class':'precip'}).string
			tenkilist.append(tmp)
		return tenkilist, c


	def embed_builder(self):
		tl, c = self.tenki_list()
		embed = Embed(colour=0x793DB6)
		a = embed.add_field
		for tenki in tl:
			a(name=tenki['city'], value=f'{tenki["climate"]}　\
					{tenki["temp"]["high"]}~{tenki["temp"]["low"]}°　\
					{tenki["precipitation"]}',
				inline=False
			)
		return embed, c


	def message_builder(self):
		"""
		Alternative method for embed_builder as this has bugs.
		"""
		tl, c = self.tenki_list()
		message = ''
		for tenki in tl:
			message += f'{tenki["city"]} {tenki["climate"]}' \
					f'{tenki["temp"]["high"]}~{tenki["temp"]["low"]}°' \
					f'{tenki["precipitation"]}'
		return message, c


class Weather(commands.Cog):
	__slots__ = ('bot', 'logger', 'last_sent_date')
	
	def __init__(self, bot):
		self.bot = bot
		self.logger = Logger(self.__class__.__name__)
		self.last_sent_date = None
		self.weather_task.start()


	@commands.command()
	async def weather(self, ctx):
		""" 天気を教えるよ！ """
		self.logger.debug('Creating weather embed.')
		scraper = Scrape_weather()
		e, c = scraper.embed_builder()
		self.logger.debug('Created weather embed.')
		await ctx.send('```' + c + '```', embed=e)
		del scraper, e, c


	@tasks.loop(seconds=50)
	async def weather_task(self):
		print('Starting weather task.')
		now = datetime.datetime.now(tz=tz)
		if not (now.hour == 6 and now.minute == 30):
			return
		if self.last_sent_date == now.date():
			return
		else:
			self.last_sent_date = now.date()
			
		scraper = Scrape_weather()
		e, c = scraper.embed_builder()
		for guild in self.bot.guilds:
			for channel in guild.channels:
				if channel.name == 'main':
					await channel.send('```' + c + '```', embed=e)
		del scraper, e, c