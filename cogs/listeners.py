import discord
from discord.ext import commands

from scripts.logger import Logger

attachmentpath = 'attachments/'


# A listener class for the bot's listener methods.
class Listener(commands.Cog):
	__slots__ = ('bot', 'logger')
	
	def __init__(self, bot):
		self.bot = bot
		self.logger = Logger(__name__)

	@commands.Cog.listener()
	async def on_ready(self):
		print('----------')
		print('Logged in as')
		print('name:\t' + self.bot.user.name)
		print('id:\t' + str(self.bot.user.id))
		print('----------')

	@commands.Cog.listener()
	async def on_message(self, mes):
		self.logger.info(f'Message:{mes.content} author:{mes.author.name} id:{mes.author.id}')

	@commands.Cog.listener()
	async def on_command_error(self, ctx, error):
		pass

	@commands.Cog.listener()
	async def on_member_remove(self, member):
		self.logger.info(f'Member removed:{member.name} id:{member.id}')

	@commands.Cog.listener()
	async def on_raw_message_delete(self, payload):
		message = payload.cached_message
		if message:
			self.logger.info(f'Message deleted:{message.content} author:{message.author.id}')
		else:
			self.logger.info('Message deleted. No content found.')
