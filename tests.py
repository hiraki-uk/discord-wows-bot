import unittest
from init.api.api import Api
from init.maps.map_db import MapDB
from config.config import get_config

class TestGetConfig(unittest.TestCase):
    def test_get_config(self):
        conf = get_config()
        self.assertFalse(conf['debug'])
        
# class TestApi(unittest.TestCase):
#     def setUp(self):
#         self.api = Api()
    
#     def test_ship_id_str_pages(self):
#         result = self.api.get_ship_id_str_pages()
#         self.assertIsInstance(result, int)
    
#     def test_fetch_ship_info(self):
#         # pass as takes long
#         pass

#     def test_fetch_maps(self):
#         result = self.api.fetch_maps()
#         print(len(result))
#         self.assertIsInstance(result, dict)


# class TestMapDB(unittest.TestCase):
#     def setUp(self) -> None:
#         self.db = MapDB()
    
#     def test_get_image(self):
#         imges = self.db.get_image('O')
#         self.assertIsInstance(imges, list)

#         img = self.db.get_image('Oc')
#         self.assertIsInstance(img, bytes)



if __name__ == '__main__':
    unittest.main()