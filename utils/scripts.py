"""
Scripts module for storing useful methods.
"""


async def add_cogs(bot, *cogs):
    """
    Add cogs to bot.
    """
    for cog in cogs:
        await bot.add_cog(cog)

def get_debug_channel(bot):
	return bot.get_channel(618259750546702336)

def get_guild(bot):
	return bot.get_guild(479603954523832320)

def get_mitsubabot(bot):
	return get_guild(bot).get_member(542828851852607499)

def get_tofu(bot):
	return get_guild(bot).get_member(558122598651920404)
