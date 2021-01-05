import json
import os
import unittest

from dotenv import load_dotenv
from PIL import Image

from gameparams.gp_db import GameparamsDB
from gameparams.images import create_image, process_image
from gameparams.warship_db import WarshipDB
from utils.member import Member
from utils.members_mamager import MembersManager

env_path = '.env'
load_dotenv(dotenv_path=env_path)

key = os.getenv('WOWS_APPLICATION_ID')
db_path = 'wows.db'


class TestWarshipDB(unittest.TestCase):
	def setUp(self):
		self.db = WarshipDB()

	def test_get_warship(self):
		yamato = self.db.get_warship('select * from warship where nickname=?', ('Yamato',))
		self.assertIsNotNone(yamato)


class TestGPManager(unittest.TestCase):
	def setUp(self):
		self.gpm = GameparamsDB()
	
	def test_search_ship(self):
		data = self.gpm.search_ship('PJSB918')
		self.assertIsNotNone(data)

	def test_ship_to_dict(self):
		data = self.gpm.search_ship('PJSB918').to_dict()
		self.assertIsInstance(data, dict)

	def test_ship_to_json(self):
		data = self.gpm.search_ship('PJSB918').to_dict()
		temp = json.dumps(data)
		self.assertIsNotNone(temp)

	def test_search_torp(self):
		data = self.gpm.search_torp('PJPT001_Sea_Torpedo_Type93')
		self.assertIsNotNone(data)

	def test_search_ship_id_str(self):
		data = self.gpm.search_ship_id_str('ya')
		self.assertEqual(type(data), list)
		
		data = self.gpm.search_ship_id_str('yama')
		self.assertEqual(type(data), str)

	def test_get_all_mods(self):
		data = self.gpm.get_all_mods()
		self.assertNotEqual(data, [])


class TestMember(unittest.TestCase):
	def test_member(self):
		m = Member(discord_id=100, account_id=200, battles=10)
		self.assertEqual(m.to_dict(), {'discord_id':100, 'account_id':200, 'battles':10})
		self.assertEqual(m.discord_id(), 100)
		self.assertEqual(m.account_id(), 200)
		m.set_value('account_id', 201)
		m.set_battles(11)
		self.assertEqual(m.account_id(), 201)
		self.assertEqual(m.battles(), 11)


class TestMemberManager(unittest.TestCase):
	def setUp(self):
		self.mm = MembersManager()
		self.m1 = Member(discord_id=100, account_id=200)
		self.m2 = Member(discord_id=101, account_id=201)
		self.m_update = Member(discord_id=102, account_id=202)
		self.tearDown()

	def tearDown(self):
		if self.mm.is_registered(100):
			self.mm.deregister_member(100)
		if self.mm.is_registered(101):
			self.mm.deregister_member(101)
		if self.mm.is_registered(102):
			self.mm.deregister_member(102)			
		if self.mm.is_registered(103):
			self.mm.deregister_member(103)


	def test_is_registered(self):
		self.assertEqual(self.mm.is_registered(-1), False)
	
	def test_registered_members(self):
		if self.mm.is_registered(399263984366256148):
			self.assertIsNotNone(self.mm.registered_members())
		else:
			self.assertEqual(self.mm.registered_members(), [])

	def test_register_member(self):
		self.assertTrue(self.mm.register_member(self.m1))
		self.assertTrue(self.mm.deregister_member(100))

	def test_update_member(self):
		self.mm.register_member(self.m_update)
		self.m_update.set_value('account_id', self.m_update.account_id()+1)
		self.assertTrue(self.mm.update_member(self.m_update))
		
	def test_update_members(self):
		self.mm.register_member(self.m_update)
		ms = self.mm.registered_members()
		for m in ms:
			if m.discord_id() == 103:
				m.set_value('account_id', m.account_id()+1)
		self.assertTrue(self.mm.update_members(ms))
		

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
