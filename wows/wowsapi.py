from scripts.logger import Logger
from wowspy import Wows, Region


class WowsAPI(Wows):
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

	def get_ship_info(self, ship_name):
		self.logger.debug(f'Creating ship_info for {ship_name}.')