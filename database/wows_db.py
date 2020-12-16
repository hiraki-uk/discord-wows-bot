import traceback

from utils.exceptions import ScrapingException
from utils.logger import Logger

from database.data import Data
from utils.database import Database
from database.scrape_facebook import get_facebook_articles
from database.scrape_medium import get_medium_articles
from database.scrape_wowshp import get_hp_articles


class Wows_database:
	"""
	Scrapes and registers data into database.
	"""
	__slots__ = ('database', 'logger')

	def __init__(self, db_path):
		self.database = Database(db_path)
		self.logger = Logger(self.__class__.__name__)
		# if db file not found or empty, create file
		try:
			with open(db_path, 'rb') as f:
				if f.read() == b'':
					self._create_table()
		except Exception as e:
			self.logger.info('Database not found.')
			self._create_table()


	async def update(self):
		"""
		Update database.
		"""
		self.logger.info('Update started.')
		try:
			# await self._update_medium()
			# await self._update_facebook()
			await self._update_hp()
		except Exception:
			self.logger.critical(f'Exception while updating: {traceback.format_exc()}')
		self.logger.info('Update finished.')


	def _create_table(self):
		self.logger.debug('Creating wows database table.')
		self.database.executescript("""
		CREATE TABLE wowsnews(
			id INTEGER PRIMARY KEY AUTOINCREMENT,
			source TEXT,
			title TEXT,
			description TEXT,
			url TEXT,
			img TEXT
		);
		""")
		self.logger.debug('Created wows database table.')

	
	def _get_latest(self, source:str):
		"""
		Get latest news stored in database.

		Returns
		-------
		res : tuple, None
		"""
		self.logger.debug(f'Starting _get_latest source: {source}')
		res = self.database.fetchone('SELECT * FROM wowsnews WHERE source==? ORDER BY id DESC', (source,))
		self.logger.debug(f'_get_latest result: {res}')
		
		return res


	def get_latest_id(self):
		"""
		Get latest news' id.
		"""
		self.logger.debug('Starting get_latest_id.')		
		res = self.database.fetchone('SELECT id FROM wowsnews ORDER BY id DESC')
		self.logger.debug(f'{res=}')
		res = res[0]
		
		return res


	def get_news(self, news_id:int):
		"""
		"""
		self.logger.debug('Starting get_news.')
		res = self.database.fetchone('SELECT * FROM wowsnews WHERE id==?', values=(news_id,))
		if res:
			data = Data(res)		
			return data
		else:
			return
		
		
	async def _update_hp(self):
		"""
		Check for new articles, if found update db.
		"""
		self.logger.info('Updating wows hp.')
		# get data and data from db.
		try:
			data = get_hp_articles()
		except ScrapingException:
			self.logger.critical('Scraping failed.')
			return
		data_db = self._get_latest('wowshomepage')
		
		# if database is up to date return
		if _is_same_data(data_db, data[0]):
			self.logger.info('Wows hp is up to date.')
			return
		# if same url already exists in database, return
		elif self._url_exists(data[0][3]):
			self.logger.info('Article with same url exists.')
			return
		# update db
		self.logger.info('Saving data.')
		try:
			self.database.execute('INSERT INTO wowsnews(source, title, description, url, img) VALUES(?, ?, ?, ?, ?)', data[0])
		except Exception as e:
			self.logger.critical(f'Inserting into database failed: {e}')
			return
		self.logger.info('Updated wows hp.')


	async def _update_facebook(self):
		"""
		Check for new articles, if found update db.
		"""
		self.logger.info('Updating facebook.')
		try:
			data = get_facebook_articles()
		except ScrapingException:
			self.logger.critical('Scraping failed.')
			return
		data_db = self._get_latest('facebook')

		# if up to date, return
		if _has_same_url(data_db, data[0]):
			self.logger.info('Facebook is up to date.')
			return
		# counter shows how many articles to update
		counter = 0
		for d in data:
			# if data is most recent in db
			if d == data_db:
				break
			counter += 1
		# data.reverse() not working, so using temp.reverse()
		temp = data
		temp.reverse()
		news = temp[:counter]
		# update db
		try:
			for new in news:
				# continue if url already exists in database
				if self._url_exists(new[3]):
					self.logger.info('Article with same url exists.')
					continue
				self.database.execute('INSERT INTO wowsnews(source, title, description, url, img) VALUES(?, ?, ?, ?, ?)', new)
		except Exception as e:
			self.logger.critical(f'Inserting into database failed: {e}')
			return
		self.logger.info('Updated facebook.')


	async def _update_medium(self):
		"""
		Check for new articles, if found update db.
		"""
		self.logger.info('Updating medium.')
		try:
			data = get_medium_articles()
		except ScrapingException:
			self.logger.critical('Scraping failed.')
			return

		# get latest data in database
		data_db = self._get_latest('medium')
		# if up to date, return
		if _is_same_data(data_db, data[0]):
			self.logger.info('Medium is up to date.')
			return
		# counter shows how many articles to update
		counter = 0
		for d in data:
			# if url is most recent in db
			if d == data_db:
				break
			counter += 1
		# data.reverse() not working, so using temp reverse()
		temp = data
		temp.reverse()
		news = temp[:counter]
		try:
			for new in news:
				self.database.execute('INSERT INTO wowsnews(source, title, description, url, img) VALUES(?, ?, ?, ?, ?)', new)
		except Exception as e:
			self.logger.critical(f'Inserting into database failed: {e}')
			return
		self.logger.info('Updated medium.')


	def _url_exists(self, url:str):
		self.logger.debug('Checking if url already exists in database.')
		self.logger.debug(f'url is {url[10:]}')
		try:
			res = self.database.fetchone(f'SELECT * FROM wowsnews WHERE url==?', (url,))
		except Exception as e:
			self.logger.critical(f'Fetching datbase failed: {e}')
			res = None
		self.logger.debug(f'Result: {res}')
		if not res:
			return False
		return True

	
def _is_same_data(data_from_db:tuple, data:tuple):
	"""
	Returns true if two data are the same excluding the id.
	Else returns false.
	"""
	if data_from_db == None:
		return False
	temp = tuple(data_from_db[1:])
	if temp != data:
		return False
	return True


def _has_same_url(data_from_db:tuple, data:tuple):
	"""
	Returns true if two data share the same url.
	Else returns false.

	This method is craeted for comparing facebook data as
	_is_same_data return false for same article where
	pic url are different.
	"""
	if data_from_db == None:
		return False
	temp = tuple(data_from_db[1:])
	if temp[3] != data[3]:
		return False
	return True
