from scripts.logger import Logger
from wows.wowsapi import Wows_API
from wows.wowsdb import Wows_database


class Wows:
    def __init__(self):
        self.wowsapi = Wows_API()
        self.wowsdb = Wows_database()
        self.logger = Logger(self.__class__.__name__)
    
    def update_warships(self):
        """
        Update warships table in database.
        """
        self.logger.debug('Updating warships in database.')
        # check version
        version_db = self.wowsdb.get_db_version()
        version_api = self.wowdapi.get_api_version()
        
        # return if version is up to date.
        if version_db == version_api:
            self.logger.debug(f'Database has latest version {version_db}'.)
            return
        
        # update version in database then update warships
        self.wowsdb.update_version(version_api)
        warships = self.wowsapi.get_warships()
        self.wowsdb.update_warships(warships)
        
        self.logger.debug('Warships updated.')

