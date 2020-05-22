from logging import Formatter, handlers, StreamHandler, getLogger, DEBUG, INFO, CRITICAL

class Logger:
	__slots__ = ('logger',)

	def __init__(self, name=__name__):
		self.logger = getLogger(name)
		self.logger.setLevel(INFO)
		formatter = Formatter("[%(asctime)s] [%(name)s] [%(levelname)s] %(message)s")

		# stdout
		handler = StreamHandler()
		handler.setLevel(INFO)
		handler.setFormatter(formatter)
		self.logger.addHandler(handler)

		# file
		handler = handlers.RotatingFileHandler(filename='artesia_bot.log',
												encoding='utf-8',
												# maxBytes=1048576,
												backupCount=1)
		handler.setLevel(INFO)
		handler.setFormatter(formatter)
		self.logger.addHandler(handler)
		del formatter, handler

	def debug(self, msg):
		self.logger.debug(msg)
	
	def info(self, msg):
		self.logger.info(msg)
	
	def warn(self, msg):
		self.logger.warning(msg)

	def critical(self, msg):
		self.logger.critical(msg)