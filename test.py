import os
import unittest

from dotenv import load_dotenv

from wows.worldofwarships import WorldofWarships
from wows.wowsapi import WowsApi
from wows.wowsdb import Wows_database

env_path = '.env'
load_dotenv(dotenv_path=env_path)

key = os.getenv('WOWS_APPLICATION_ID')
db_path = 'wows.db'


# class TestWowsApi(unittest.TestCase):
# 	def test_warships_count(self):
# 		w = WowsApi(key)
# 		res = w.get_warships_count()
# 		self.assertNotEqual(res, None)

# 	def test_get_warships(self):
# 		w = WowsApi(key)
# 		res = w.get_warships(1)
# 		self.assertNotEqual(res, None)

# 	def test_get_shipprofile(self):
# 		w = WowsApi(key)
# 		res = w.get_ship_profile(3248371408)
# 		self.assertNotEqual(res, None)
# 	def test_info_about_encyclopedia(self):
# 		w = WowsApi(key)
# 		res = w.information_about_encyclopedia()
# 		self.assertNotEqual(res, None)


# class TestWowsDb(unittest.TestCase):
# 	def test_get_db_version(self):
# 		w = Wows_database(db_path)
# 		res = w.get_db_version()
# 		self.assertNotEqual(res, None)
	
# 	def test_get_warship(self):
# 		w = Wows_database(db_path)
# 		res = w.get_warship('Georgia')
# 		self.assertNotEqual(res, None)
# 		res = w.get_warship('G')
# 		self.assertNotEqual(res, None)

# 	def test_get_warships(self):
# 		w = Wows_database(db_path)
# 		res = w.get_warships()
# 		self.assertNotEqual(res, None)

# 	def test_get_ship_ids(self):
# 		w = Wows_database(db_path)
# 		res = w.get_ship_ids()
# 		self.assertNotEqual(res, None)

# 	def test_get_ship_param(self):
# 		w = Wows_database(db_path)
# 		res = w.get_shipparam(3248371408)
# 		self.assertNotEqual(res, None)



		
if __name__ == '__main__':
	unittest.main()