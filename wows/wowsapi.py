from scripts.logger import Logger
from wowspy import Wows, Region
import math
import json


class Wows_API(Wows):
	def __init__(self, key):
		self.logger = Logger(self.__class__.__name__)
		

	def get_player_info(self, player_name):
		self.logger.debug(f'Creating player info for {player_name}.')
		player = self.players(Region.AS, player_name)
		if not player:
			return
		elif player['status'] != 'ok':
			return
		player_id = player['data'][0]['account_id']
		player_data = self.player_personal_data(Region.AS, player_id)
		if not player_data:
			return
		elif player_data['status'] != 'ok':
			return
		player_data = player_data['data'][str(player_id)]
		self.logger.debug('Created player_data successfully.')
		return player_data
	
	def get_api_version(self):
		"""
		Get api's version.
		"""
		result = self.information_about_encyclopedia(Region.AS, fields='ships_updated_at')
		if result['status'] != 'ok':
			self.logger.info('Status for api returned an error.')
			return
		version = result['data']['ships_updated_at']
		return version

	def get_warships(self):
		"""
		Get warships fetched from wows api.
		"""
		self.logger.debug('Fetching for warships.')
		warships = []
		temp = self.warships(Region.AS, fields='name', limit=1)
		if temp['status'] != 'ok':
			self.loger.info('Status for api returned an error.')
			return

		pages = math.ceil(warships_count/100) 
		for i in range(pages):
			temp = self.warships(Region.AS, page_no=i)
			if temp['status'] != 'ok':
				self.logger.info('Status for api returned an error.')
				return
			data = temp['data']
			warships.extend(data)
		return warships

	def get_ship_info(self, ship_name):
		self.logger.debug(f'Creating ship_info for {ship_name}.')
