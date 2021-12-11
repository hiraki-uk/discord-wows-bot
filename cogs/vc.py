from discord.ext import commands
from utils.logger import Logger

# import youtube_dl


class VoiceChannel(commands.Cog):
	__slots__ = ('bot', 'logger')
	
	def __init__(self, mitsuba):
		self.bot = mitsuba.bot
		self.logger = Logger(self.__class__.__name__)

		
	# change voice channel's bit rate
	@commands.command(aliases=['ビットレート', 'びっとれーと'])
	async def bitrate(self, ctx, bitrate=None):
		""" 今いるvcのビットレートを変更するよ！ """
		try:
			vc = ctx.author.voice.channel
		except:
			await ctx.send('ハゲろ！')
			return			
		if vc == None:
			await ctx.send('vcに入ってないとこの機能は使えないよ！')
			return
		if bitrate == None:
			await ctx.send('現在のビットレートは' + f'{vc.bitrate // 1000}' + 'kbpsだよ！')
			return
		try:
			bitrate = int(bitrate)
		except:
			await ctx.send('ビットレートを変更するには8から96までの数字を入力してね！')
			return
		if not (8 <= bitrate & bitrate <= 96):
			await ctx.send('ビットレートは8から96までだよ！')
			return
			
		await ctx.author.voice.channel.edit(bitrate=bitrate * 1000)
		await ctx.send(':thumbsup:')


# # Suppress noise about console usage from errors
# youtube_dl.utils.bug_reports_message = lambda: ''


# ytdl_format_options = {
# 	'format': 'bestaudio/best',
# 	'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
# 	'restrictfilenames': True,
# 	'noplaylist': True,
# 	'nocheckcertificate': True,
# 	'ignoreerrors': False,
# 	'logtostderr': False,
# 	'quiet': True,
# 	'no_warnings': True,
# 	'default_search': 'auto',
# 	'source_address': '0.0.0.0' # bind to ipv4 since ipv6 addresses cause issues sometimes
# }

# ffmpeg_options = {
# 	'options': '-vn'
# }

# ytdl = youtube_dl.YoutubeDL(ytdl_format_options)


# class YTDLSource(discord.PCMVolumeTransformer):
# 	def __init__(self, source, *, data, volume=0.5):
# 		super().__init__(source, volume)

# 		self.data = data

# 		self.title = data.get('title')
# 		self.url = data.get('url')

# 	@classmethod
# 	async def from_url(cls, url, *, loop=None, stream=False):
# 		loop = loop or asyncio.get_event_loop()
# 		data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))

# 		if 'entries' in data:
# 			# take first item from a playlist
# 			data = data['entries'][0]

# 		filename = data['url'] if stream else ytdl.prepare_filename(data)
# 		return cls(discord.FFmpegPCMAudio(filename, **ffmpeg_options), data=data)


# class Music(commands.Cog):
# 	def __init__(self, bot):
# 		self.bot = bot

# 	@commands.command()
# 	async def join(self, ctx):
# 		"""Joins a voice channel"""

# 		if ctx.voice_client is not None:
# 			return await ctx.voice_client.move_to(ctx.author.voice.channel)

# 		await ctx.author.voice.channel.connect()

# 	# @commands.command()
# 	# async def play(self, ctx, *, query):
# 	#     """Plays a file from the local filesystem"""

# 	#     source = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(query))
# 	#     ctx.voice_client.play(source, after=lambda e: print('Player error: %s' % e) if e else None)

# 	#     await ctx.send('Now playing: {}'.format(query))

# 	@commands.command()
# 	async def play(self, ctx, url):
# 		"""Plays from a url (almost anything youtube_dl supports)"""

# 		async with ctx.typing():
# 			print('downloading...')
# 			player = await YTDLSource.from_url(url, loop=self.bot.loop)
# 			print('playing...')
# 			ctx.voice_client.play(player, after=lambda e: print('Player error: %s' % e) if e else None)

# 		await ctx.send('Now playing: {}'.format(player.title))

# 	# @commands.command()
# 	# async def stream(self, ctx, *, url):
# 	#     """Streams from a url (same as yt, but doesn't predownload)"""

# 	#     async with ctx.typing():
# 	#         player = await YTDLSource.from_url(url, loop=self.bot.loop, stream=True)
# 	#         ctx.voice_client.play(player, after=lambda e: print('Player error: %s' % e) if e else None)

# 	#     await ctx.send('Now playing: {}'.format(player.title))

# 	@commands.command()
# 	async def volume(self, ctx, volume: int):
# 		"""Changes the player's volume"""

# 		if ctx.voice_client is None:
# 			return await ctx.send("Not connected to a voice channel.")

# 		ctx.voice_client.source.volume = volume / 100
# 		await ctx.send("Changed volume to {}%".format(volume))

# 	@commands.command()
# 	async def stop(self, ctx):
# 		"""Stops and disconnects the bot from voice"""

# 		await ctx.voice_client.disconnect()

# 	# @play.before_invoke
# 	@play.before_invoke
# 	# @stream.before_invoke
# 	async def ensure_voice(self, ctx):
# 		if ctx.voice_client is None:
# 			if ctx.author.voice:
# 				await ctx.author.voice.channel.connect()
# 			else:
# 				await ctx.send("You are not connected to a voice channel.")
# 				raise commands.CommandError("Author not connected to a voice channel.")
# 		elif ctx.voice_client.is_playing():
# 			ctx.voice_client.stop()
