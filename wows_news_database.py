import asyncio

from database.db_manager import Database_manager


if __name__ == '__main__':
	db = Database_manager('database/wows.db')

	loop = asyncio.get_event_loop()
	try:
		loop.run_until_complete(
				db.start()
		)
	except KeyboardInterrupt:
		pass
	finally:
		loop.close()
 