"""
Scripts module for storing useful methods.
"""

role_upper_bound = 537488556608716801
role_lower_bound = 569315869314908160


def add_cogs(bot, *cogs):
    """
    Add cogs to bot.
    """
    for cog in cogs:
        bot.add_cog(cog)

def get_debug_channel(bot):
	return bot.get_channel(618259750546702336)

def get_guild(bot):
	return bot.get_guild(479603954523832320)


def get_activity_role(bot, member):
	"""
	Returns the activity_role which given member has.
	"""
	role = member.top_role
	# if the top role is not role_lower_bound, that's activity role
	activity_role = role if role.id == role_lower_bound else None

	return activity_role


async def remove_activity_role(bot, member):
		role = get_activity_role(bot, member)
		if role:
			await member.remove_roles(role)


async def give_activity_role(bot, member, activity_name):
	# give activity if same already exists
	roles = get_guild(bot).roles
	roles.reverse()

	for role in roles:
		# when activity matches give that
		if role.name == activity_name:
			member.add_roles(role)
			return
		# when lower_bound is found, create and give that
		elif role.id == role_lower_bound:
			await get_guild(bot).create_role(name=activity_name,)

