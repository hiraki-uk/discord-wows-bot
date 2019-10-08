import sqlite3
import traceback
from sqlite3 import Connection

from scripts.logger import Logger


class Database:
	"""
	Database class.
	"""
	def __init__(self, db_path:str, logger=None):
		self.db_path = db_path
		self.logger = Logger(__name__) if logger is None else logger


	def fetchone(self, command:str, values=()):
		"""
		Get one result from database.
		"""
		self.logger.debug(f'Executing script on {self.db_path}.')
		# connect and execute script
		try:
			conn = self._create_connection()
			cursor = conn.cursor()
			cursor.execute(command, values)
			result = cursor.fetchone()
		# sql errors
		except Exception as e:
			self.logger.critical(e)
			self.logger.critical(traceback.format_exc())
			result = None
		# close connection
		finally:
			self._close_connection(conn)

		self.logger.debug(f'Executing script finished on {self.db_path}.')
		return result


	def execute(self, command:str, values=()):
		"""
		Get one result from database.
		"""
		self.logger.debug(f'Executing script on {self.db_path}.')
		# connect and execute script
		try:
			conn = self._create_connection()
			cursor = conn.cursor()
			cursor.execute(command, values)
		# sql errors
		except Exception as e:
			self.logger.critical(e)
			self.logger.critical(traceback.format_exc())
			result = None
		# close connection
		finally:
			self._close_connection(conn)

		self.logger.debug(f'Executing script finish on {self.db_path}.')


	def executescript(self, command:str):
		"""
		Execute script on database.
		"""
		self.logger.debug(f'Executing script on {self.db_path}.')
		# connect and execute script
		try:
			conn = self._create_connection()
			cursor = conn.cursor()
			cursor.executescript(command)
		# sql errors
		except Exception as e:
			self.logger.critical(e)
			self.logger.critical(traceback.format_exc())
			result = None
		# close connection
		finally:
			self._close_connection(conn)

		self.logger.debug(f'Executing script finished on {self.db_path}.')


	def _create_connection(self) -> Connection:
		self.logger.debug('Connecting to database.')
		conn = sqlite3.connect(self.db_path)
		self.logger.debug('Connected to database.')
		return conn


	def _close_connection(self, conn):
		self.logger.debug('Closing connection to database.')
		conn.commit()
		conn.close()
		self.logger.debug('Closed connection to database.')
