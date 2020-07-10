import os

from dotenv import load_dotenv

from wows.worldofwarships import WorldofWarships
from wows.wowsdb import Wows_database

env_path = '.env'
load_dotenv(dotenv_path=env_path)

key = os.getenv('WOWS_APPLICATION_ID')
db_path = 'wows.db'


def update_wows():
	print('Updating wows.')
	w = WorldofWarships(key, db_path)	
	w.update()
	print('Updated wows.')
def update_modules():
	print('Updating modules.')
	w = WorldofWarships(key, db_path)
	w.update_modules()
	print('Updated modules.')


if __name__ == '__main__':
	update_wows()
	update_modules()
