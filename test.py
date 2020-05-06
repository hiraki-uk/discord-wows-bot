import os
import unittest

from dotenv import load_dotenv

from wows.worldofwarships import WorldofWarships

env_path = '.env'
load_dotenv(dotenv_path=env_path)

key = os.getenv('WOWS_APPLICATION_ID')
db_path = 'wows.db'
class TestWows(unittest.TestCase):
	def test_wows(self):
		w = WorldofWarships(key, db_path)
		w.update_warships()
		version = w.wowsdb.get_db_version()
		self.assertNotEqual(version, 0)
		os.remove(db_path)			