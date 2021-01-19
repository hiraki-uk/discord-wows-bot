# from gameparams.images import *
from utils.database import Database

from .api import Api

path = 'res/id_api.db'


def create_api_db():
	"""
	Create id_api.db file.
	"""
	wows = Api()
	db = ApiDB()
	db.init_db()
	
	# get total number of pages
	result = wows.get_ship_id_str_pages()
	if result is None: return
	ships = []
	# fetch each page, save ship data
	for page in range(result):
		result = wows.fetch_ship_info(page+1)
		if result is None: return
		ships.extend(result)
	db.insert_data(ships)


class ApiDB:
	def __init__(self) -> None:
		self.db = Database(path)

	def init_db(self):
		self.db.execute('DROP TABLE IF EXISTS ships')
		self.db.executescript("""CREATE TABLE ships(
			id_int INTEGER PRIMARY KEY,
			name TEXT,
			id_str TEXT,
			img BLOB,
			img_final BLOB)""")


	def insert_data(self, ships):
		command = 'INSERT INTO ships (id_int, name, id_str, img, img_final) VALUES (?,?,?,?,?)'
		l = [(
				command,
				(ship['id'], ship['name'], ship['id_str'], ship['img'], ship['img_final'])
			) for ship in ships]
		self.db.insertmany(l)

	def list_all_ships(self):
		"""
		Get list of IMPLEMENTED SHIPS ONLY
		"""
		command = 'SELECT name, id_str FROM ships'
		results = self.db.fetchall(command)
		return results

	
	def get_name(self, id_str):
		command = f'SELECT name FROM ships WHERE id_str=?'
		result = self.db.fetchone(command, values=(id_str,))
		if result:
			return result[0]


	def process_images(self, warshipdb):
		"""
		Process all images in database.
		"""
		l = []
		results = self.db.fetchall('SELECT id_int, img FROM ships') # [(id, img), (id, img), ...]
		# for every ship create image
		for id_int, img in results:
			# get warship of it
			warship = warshipdb.get_warship(f'SELECT * FROM warship WHERE shipid=?', (id_int,))
			# if warship not found, continue
			if not warship:
				continue
			# resize, enhance
			processed_img = process_image(img, warship)
			l.append((
				f'UPDATE ships SET img_final=? WHERE id_int={id_int}',
				(processed_img,)))
		self.db.insertmany(l)

	
	def get_image_fin(self, name):
		result = self.db.fetchone('SELECT img_final FROM ships WHERE name=?', (name,))
		if len(result) == 1:
			return result[0]


	def get_image(self, name):
		"""
		Get image.
		"""
		result = self.db.fetchall(f'SELECT name FROM ships WHERE name like ?', (f'%{name}%',))
		results = list(map(lambda x: x[0], result))
		# if one hit, return it
		if len(results) == 1:
			img = self.get_image_fin(results[0])
			return img
		else:
			names = [n for n in results if
				not n.startswith('[') and
				not n.endswith(' B') and
				not n.startswith('ARP ')]
			# if exact match
			if len(names) == 1:
				img = self.get_image_fin(names[0])
				return img
			for n in names:
				if n.lower() == name.lower():
					img = self.get_image_fin(n)
					return img
			return names
