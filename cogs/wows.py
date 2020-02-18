import discord
from discord.ext import commands, tasks
from wowspy.wowspy import Wows, Region

from cogs.cogfunctions.database import Database
from scripts.logger import Logger

wowsdb_name = 'temp.db'


class WorldOfWarships(Commands.Cog):
    """
    World of Warships Cog class.
    Registers and deregisteres users into database.
    """
    def __init__(self, bot):
        self.bot = bot
        self.wowsdbmanager = WowsDbManager()
        self.wows = Wows(key='key')


    @commands.Command()
    async def register(self, ctx, ign=None):
        """
        Register user into database.
        """
        if ign is None:
            await ctx.send('No ign!')
            return
        # fetch wows id
        player = self.wows.players(Region.AS, ign)

        if player is None:
            await ctx.send('No player found!')
            return
        elif player.status == 404:
            await ctx.send('try again later')
            return
        wows_id = player.wows_id
        discord_id = ctx.discord_id
        self.wowsdbmanager.register(wows_id, discord_id)


    @commands.Command()
    async def deregister(self, ctx):
        """
        Deregister user from database.
        """ 
        discord_id = ctx.discord_id
        self.wowsdbmanager.deregister(discord_id)


class WowsDbManager:
    """
    World of warships database manager class.
    Responsible for communication between Cog and database.
    """
    def __init__(self):
        self.db = WowsDatabase()


    def register(self, wows_id:int, discord_id:int):
        """
        Register user into database.

        Parameters
        ----------
        wows_id : int
            Player's id.
        discord_id : int
            Discord user's id.

        Raises
        ------
        PlayerRegisteredException
            Raised if the player is already registered.
        """
        if self.db.is_registered(discord_id):
            raise PlayerRegisteredException

        self.db.register(wows_id, discord_id)


    def deregister(self, discord_id:int):
        """
        Deregister user from database.

        Parameters
        ----------
        discord_id : int
            Player's id.

        Raises
        ------
        PlayerNotRegisteredException
            Raised if the player is not registered.
        """
        if not self.db.is_registered(discord_id):
            raise PlayerNotRegisteredException

        self.db.deregister(discord_id)


class WowsDatabase:
    def __init__(self):
        self.db = Database(wowsdb_name)


    def register(self, wows_id:int, discord_id:int):
        """
        Register wows_id and discord_id into database.
        """
        self.db.execute('INSERT INTO players', (wows_id, discord_id))


    def deregister(self, wows_id:int, discord_id:int):
        """
        Deregister wows_id into database.
        """
        self.db.execute('')    


    def is_registered(self, discord_id:int):
        """
        Check if discord_id is already registered in database.
        """
        result = self.db.execute('SELECT * FROM players WHERE discord_id = (?)', (discord_id,))
        return result is None


class PlayerNotRegisteredException(Exception):
    pass
class PlayerRegisteredException(Exception):
    pass
