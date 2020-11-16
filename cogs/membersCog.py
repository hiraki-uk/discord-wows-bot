import datetime

from discord.ext import commands, tasks
from utils.logger import Logger
from utils.member import Member
from utils.members_mamager import MembersManager

from wows.wowsapi import WowsApi

tz = datetime.timezone(datetime.timedelta(hours=9))


class MembersCog(commands.Cog):
	def __init__(self, bot, key):
		self.bot = bot
		self.logger = Logger(self.__class__.__name__)
		self.api = WowsApi(key)
		self.members_manager = MembersManager()
		self.last_sent_date = None
		self.update()
		self.wows_task.start()


	@commands.group()
	async def reg(self, ctx):
		""" 役職をいじれるよ！ """
		if ctx.invoked_subcommand is None:
			await ctx.send('コマンドも教えてね！')


	@reg.command()
	async def wows(self, ctx, wows_ign=None):
		"""
		あなたのぽふね、監視してあげる♡
		"""
		self.logger.info('Starting reg.wows command.')
		# get account_id
		account_id = self.api.get_account_id(wows_ign)
		if not account_id:
			await ctx.send('ごめんね、この名前見つからなかったぽい～')
			return
		# register user
		member = Member(discord_id=ctx.message.author.id, account_id=account_id)
		if not self.members_manager.register_member(member):
			await ctx.send('あーーーーエラったごめんしあに報告して！')
			return
		await ctx.send('毎度ありがとうございます♡')


	@commands.command()
	async def ranking(self, ctx):
		await self.report(final=False, ctx=ctx)


	@tasks.loop(seconds=50)
	async def wows_task(self):
		""" Report and update members.json file. """
		now = datetime.datetime.now(tz=tz)
		if not (now.weekday() == 0 and now.hour == 7 and now.minute == 0):
			return
		if self.last_sent_date == now.date():
			return
		else:
			self.last_sent_date = now.date()

		await self.report()
		self.update()


	async def report(self, final=True, ctx=False):
		# check for all registered members
		members = self.members_manager.registered_members()
		report_list = []
		for member in members:
			account_id = member.account_id()
			ign = self.api.get_in_game_name(account_id)
			battles = self.api.get_battle_count(account_id)
			if not battles == 0 or not member.battles() == 0:
				weekly_battles = battles - member.battles()
			else:
				weekly_battles = 0
			report_list.append((ign, weekly_battles))
		if len(report_list) < 5:
			return
		if final:
			message = '週間戦闘数ランキングはっぴょー！！！！！\n\n'
		else:
			message = '戦闘数ランキング中間はっぴょー！！！！！\n\n'
		report_list.sort(reverse=True, key=lambda x: x[1])
		message += f'||**__一位！ {report_list[0][0]}\t{report_list[0][1]}戦__**||\n\n' \
					f'```二位！ {report_list[1][0]}\t{report_list[1][1]}戦\n' \
					f'三位！ {report_list[2][0]}\t{report_list[2][1]}戦\n' \
					f'四位！ {report_list[3][0]}\t{report_list[3][1]}戦\n' \
					f'五位！ {report_list[4][0]}\t{report_list[4][1]}戦\n```'
		if ctx:
			await ctx.send(message)
		for guild in self.bot.guilds:
			for channel in guild.channels:
				if channel.name == 'bot-room':
					await channel.send(message)


	def update(self):
		members = self.members_manager.registered_members()
		for member in members:
			account_id = member.account_id()
			member.set_battles(self.api.get_battle_count(account_id))
		self.members_manager.update_members(members)