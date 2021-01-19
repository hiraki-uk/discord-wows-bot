import sqlite3
import traceback
from sqlite3 import Connection

from utils.logger import Logger


class Database:
	"""
	Database class.
	"""
	def __init__(self, db_path:str):
		self.db_path = db_path
		self.logger = Logger(self.__class__.__name__)


	def fetchone(self, command:str, values=()):
		"""
		Get one result from database.
		"""
		# connect and execute script
		conn = None
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
		return result


	def fetchall(self, command:str, values=()):
		"""
		Get all results from database.
		"""
		# connect and execute script
		conn = None
		try:
			conn = self._create_connection()
			cursor = conn.cursor()
			cursor.execute(command, values)
			result = cursor.fetchall()
		# sql errors
		except Exception as e:
			self.logger.critical(e)
			self.logger.critical(traceback.format_exc())
			result = None
		# close connection
		finally:
			self._close_connection(conn)
		return result


	def execute(self, command:str, values=()):
		"""
		Get one result from database.
		"""
		# connect and execute script
		conn = None
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


	def executescript(self, command:str):
		"""
		Execute script on database.
		"""
		# connect and execute script
		conn = None
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

	
	def insertmany(self, l:list):
		"""
		Inserts many data into database.

		Params
		------
		l : list
			l = [(command, val), (command, val), ...]
		"""
		conn = self._create_connection()
		cursor = conn.cursor()
		try:
			for command, value in l:
				cursor.execute(command, value)
		except Exception as e:
			self.logger.critical(e)
			self.logger.critical(traceback.format_exc())
		finally:
			self._close_connection(conn)


	def executemany(self, l:list):
		"""
		Executes many commands into database.

		Params
		------
		l : list
			l = [command, command, command, ...]
		"""
		conn = self._create_connection()
		cursor = conn.cursor()
		try:
			for command in l:
				cursor.execute(command)
		except Exception as e:
			self.logger.critical(e)
			self.logger.critical(traceback.format_exc())
		finally:
			self._close_connection(conn)
				

	def _create_connection(self) -> Connection:
		conn = sqlite3.connect(self.db_path)
		return conn


	def _close_connection(self, conn):
		conn.commit()
		conn.close()