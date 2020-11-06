"""
Scripts module for storing useful methods.
"""


role_upper_bound = 537488556608716801
role_lower_bound = 569315869314908160

rank_role_id = {
	'1':759886350161412156,
	'2':759886138658914344,
	'3':759886197295939634,
	'4':759886373380816906,
	'5':759886388417134633,
	'6':759886403081076827,
	'7':759886414904557608,
	'8':759886426690551860,
	'9':759886439428128779,
	'10':759886454603907073,
	'-1':759886471233667112
}


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

def get_mitsubabot(bot):
	return get_guild(bot).get_member(542828851852607499)

def get_tofu(bot):
	return get_guild(bot).get_member(558122598651920404)

def get_god_role(bot):
	return get_guild(bot).get_role(role_upper_bound)

def get_rank_role_id(rank):
	return
