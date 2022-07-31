"""
Main python file.
English description is for developers, where Japanese ones will be desplayed to users.  
"""
import asyncio

from cogs.cogs import Cogs
from cogs.listeners import Listener
from cogs.maps import MapsCog
from cogs.pdf2image import Pdf2Image
from cogs.roles import Roles
from cogs.shitposting import Shitposting
from cogs.vc import VoiceChannel
from cogs.weather import Weather
from cogs.wows import WowsCog
from init.bot_setup import Mitsuba
from utils.scripts import add_cogs

mitsuba = Mitsuba()
bot = mitsuba.bot
key = mitsuba.config['discord_bot_key']

add_cogs(bot,
	Cogs(mitsuba),
	Roles(mitsuba),
	# Pdf2Image(mitsuba),
	Listener(mitsuba),
	MapsCog(mitsuba),
	Shitposting(mitsuba),
	VoiceChannel(mitsuba),
	Weather(mitsuba),
	WowsCog(mitsuba),
)
if __name__ == '__main__':
	loop = asyncio.get_event_loop()
	try:
		loop.run_until_complete(
				mitsuba.bot.start(key)
		)
	except KeyboardInterrupt:
		loop.run_until_complete(mitsuba.bot.logout())
	finally:
		loop.close()
