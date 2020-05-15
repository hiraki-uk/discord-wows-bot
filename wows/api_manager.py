from scripts.logger import Logger
from wowspy import Wows, Region
import math
import json
import requests
from .wowsapi import WowsApi

class ApiManager:
	def __init__(self, key):
		self.logger = Logger(self.__class__.__name__)
		self.api = WowsApi(key)

	def get_player_info(self, player_name):
		self.logger.debug(f'Creating player info for {player_name}.')
		player = self.api.players(Region.AS, player_name)
		if not player:
			return
		elif player['status'] != 'ok':
			return
		player_id = player['data'][0]['account_id']
		player_data = self.api.player_personal_data(Region.AS, player_id)
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
		self.logger.debug('Fetching version for api.')
		version = self.api.information_about_encyclopedia()
		self.logger.debug('Returning api version.')
		return version

	def get_warships(self):
		"""
		Get warships fetched from wows api.
		"""
		self.logger.debug('Fetching for warships api.')
		warships = []
		warships_count = self.api.get_warships_count()
		pages = math.ceil(warships_count/100) 
		warships = self.api.get_warships(pages)
		self.logger.debug('Created warships.')
		return warships

