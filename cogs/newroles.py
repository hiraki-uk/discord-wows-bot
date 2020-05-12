from discord.ext import commands, tasks

from scripts.logger import Logger
from scripts.scripts import get_guild, get_mitsubabot, get_tofu

# 全知神
_activity_role_ceiling = 537488556608716801
# ほうれん草
_activity_role_floor = 569315869314908160


class NewRoles(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
		self.logger = Logger(__name__)

	@commands.command()
	async def dl(self, ctx):
		""" Temporal command for deleting guild activity roles. """
		ceiling = ctx.guild.get_role(632304461087506442)
		roles = ctx.guild.roles
		# for role in roles:
		# 	if role.position is not 0 and \
		# 		role < ceiling:
		# 		self.logger.debug(f'deleting {role}')
		# 		await role.delete()
		# self.logger.debug('done.')
		roles = await self._get_guild_activity_roles()
		for role in roles:
			self.logger.debug(f'deleting {role}')
			await role.delete()
		self.logger.debug('done.')
	
	@commands.command()
	async def role_task(self, ctx):
		self.logger.debug('starting role_task.')
		members = ctx.guild.members
		self.logger.debug(f'found {len(members)} members.')
		guild_activity_roles = await self._get_guild_activity_roles()
		self.logger.debug('got guild activity roles.')

		# give or remove roles
		for member in members:
			await self._configure_roles(member)

		# remove unused roles
		await self._remove_unused_activity_roles(guild_activity_roles)

		# # configure hierarchy
		# guild_activity_roles = await self._get_guild_activity_roles()
		# await self._configure_hierarchy(guild_activity_roles)

		self.logger.debug('finished role_task.')

	async def _configure_roles(self, member):
		"""
		Give or remove activity roles of the member.
		"""
		self.logger.debug('configuring roles.')
		activities = member.activities # member's activities
		anames = [a.name for a in activities]
		activity_roles = await self._get_activity_roles(member) # member's activity roles given
		rnames = [r.name for r in activity_roles]
		self.logger.debug(f'{len(anames)} activity names and {len(rnames)} role names found.')
		# removing process
		for rname in rnames:
			self.logger.debug(f'processing role name {rname}.')
			# if member has a role which the member does not play, remove
			if rname not in anames:
				self.logger.debug('removing role.')
				role = self._get_role(activity_roles, rname)
				if not role:
					self.logger.critical('role not found.')
					return
				await member.remove_role(role)
			# else, member has a role which the member plays, so pass
		
		# giving process
		for aname in anames:
			# if it was Custom status, you can't fetch the status name
			# thus skip giving process
			if aname == 'Custom Status':
				continue
			self.logger.debug(f'giving role named {aname}.')
			# if member has activity which the member does not have a role of, give that
			if aname not in rnames:
				self.logger.debug('giving role.')
				role = await self._get_opt_role(aname)
				self.logger.debug('adding role.')
				await member.add_roles(role)
				self.logger.debug('added role.')
			# else, member has activity and has role of, pass

	async def _get_opt_role(self, aname):
		"""
		Get a role where name is aname.
		If that role exists, return that.
		If it does not exist, create one and return that.
		"""
		self.logger.debug('finding for optimum role.')
		roles = await self._get_guild_activity_roles()
		for role in roles:
			if role.name == aname:
				return role
		role = await self._create_role(aname)
		return role
		
	async def _create_role(self, aname):
		"""
		Return role with given name aname and position where one larger than role_floor.
		"""
		self.logger.debug('creating role.')
		guild = get_guild(self.bot)
		self.logger.debug('found guild.')
		role = await guild.create_role(name=aname, hoist=True)
		self.logger.debug(f'created role {aname}.')
		floor_role = get_guild(self.bot).get_role(_activity_role_floor)
		self.logger.debug('found floor_role.')
		self.logger.debug(f'floor position is {floor_role.position}.')
		position = floor_role.position
		# role.edit does not work sometimes
		while position is not role.position:
			self.logger.debug(f'position is {position} and role.position is {role.position}')
			await role.edit(position=position)

		self.logger.debug('returning role.')
		return role

	def _get_role(self, activity_roles, rname):
		"""
		Get role where name is rname in activity_roles.
		Returns None if no role found.
		"""
		for arole in activity_roles:
			if arole.name == rname:
				return arole
		return None

	# merge _get_guild_activity_roles() and _get_activity_roles() later
	async def _get_guild_activity_roles(self):
		"""
		Return list of activity roles of a given guild.
		"""
		self.logger.debug('finding for guild activity roles.')
		guild = get_guild(self.bot)
		roles = guild.roles

		floor = guild.get_role(_activity_role_floor)
		ceiling = guild.get_role(_activity_role_ceiling)

		self.logger.debug(f'{len(roles)} roles found.')
		activity_roles = []
		self.logger.debug(f'floor position is {floor.position} and ceiling position is {ceiling.position}.')
		for role in roles:
			if role < ceiling \
				and floor < role:
				activity_roles.append(role)
		self.logger.debug(f'returning roles list with {len(activity_roles)} items.')
		return activity_roles

	async def _get_activity_roles(self, member):
		"""
		Return list of activity roles of a given member.
		"""
		roles = member.roles
		guild = get_guild(self.bot)
		floor = guild.get_role(_activity_role_floor)
		ceiling = guild.get_role(_activity_role_ceiling)

		activity_roles = []
		for role in roles:
			if role < ceiling \
				and floor < role:
				activity_roles.append(role)
		return activity_roles

	async def _remove_unused_activity_roles(self, guild_activity_roles):
		"""
		Removes all unused activity roles.
		"""
		for role in guild_activity_roles:
			if not role.members:
				await role.delete()
		
	async def _configure_hierarchy(self, guild_activity_roles):
		"""
		Configures hierarchy of guild's activity roles.
		Hirarchy will be configured by its number of players.
		"""
		self.logger.debug('Configuring hierarchy.')
		new_pos = get_guild(self.bot).get_role(_activity_role_floor).position
		# sort roles in order of members
		roles = sorted(guild_activity_roles, key=lambda role: len(role.members))
		roles.reverse()
		for role in roles:
			# edit role if needed
			self.logger.debug(f'{role} is at {role.position} and new position is {new_pos}')
			if not role.position == new_pos:
				await role.edit(position=new_pos)
			pos =+ 1
