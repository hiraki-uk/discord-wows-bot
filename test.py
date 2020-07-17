import json
import os
import unittest

from dotenv import load_dotenv

from wows.warship import Warship
from wows.worldofwarships import WorldOfWarships

env_path = '.env'
load_dotenv(dotenv_path=env_path)

key = os.getenv('WOWS_APPLICATION_ID')
db_path = 'wows.db'


class TestWows(unittest.TestCase):
	def test_search_warship(self):
		w = WorldOfWarships()
		s = w.search_ship('shimakaze')
		self.assertTrue(isinstance(s[0], str))
		s = w.search_ship('012_Shimakaze_1943')
		self.assertTrue(isinstance(s[0], Warship))

	def test_create_warship(self):
		w = WorldOfWarships()
		s = w.create_warship('PJSD912_Shimakaze_1943')
		self.assertTrue(isinstance(s, Warship))


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
