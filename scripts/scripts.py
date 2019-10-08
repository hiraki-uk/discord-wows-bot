"""
Scripts module for storing useful methods.
"""

def add_cogs(bot, *cogs):
    """
    Add cogs to bot.
    """
    for cog in cogs:
        bot.add_cog(cog)

