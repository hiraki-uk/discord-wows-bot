from scripts.logger import Logger
from wowspy import Wows, Region
import math
import json
import requests

class Wows_API:
	def __init__(self, key):
		self.logger = Logger(self.__class__.__name__)
		self.api = Api(key)

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


class Api:
	def __init__(self, application_id):
		self.application_id = application_id

	def get_warships_count(self):
		response = requests.get('https://api.worldofwarships.asia/wows/encyclopedia/ships/?' \
			f'application_id={self.application_id}&limit=1')
		if response.status_code != 200:
			return
		text = response.text
		text_json = json.loads(text)
		if text_json['status'] != 'ok':
			return
		warships_count = text_json['meta']['total']
		return warships_count

	def get_warships(self, pages):
		print('hello world')
		warships = []
		for i in range(pages):
			response = requests.get('https://api.worldofwarships.asia/wows/encyclopedia/ships/?' \
				f'application_id={self.application_id}&page_no={i+1}&language=ja')
			if response.status_code != 200:
				return
			text = response.text
			text_json = json.loads(text)
			if text_json['status'] != 'ok':
				return
			values = text_json['data'].values()
			warships.extend(values)
		return warships
	
	def information_about_encyclopedia(self):
		response = requests.get('https://api.worldofwarships.asia/wows/encyclopedia/info/?' \
			f'application_id={self.application_id}&fields=game_version')
		if response.status_code != 200:
			return
		text = response.text
		text_json = json.loads(text)
		if text_json['status'] != 'ok':
			return
		version = text_json['data']['game_version']
		return version
		