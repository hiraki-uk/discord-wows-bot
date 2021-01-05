import json

import requests
from wowspy import Region, Wows


class WowsApi:
	def __init__(self, key):
		self.key = key
		self.wowspy = Wows(key)


	def get_in_game_name(self, account_id):
		try:
			response = self.wowspy.player_personal_data(region=Region.AS, account_id=account_id, fields='nickname')
			if not response:
				return
			elif response['status'] != 'ok':
				return
			in_game_name = response['data'][str(account_id)]['nickname']
			return in_game_name
		except:
			return


	def get_battle_count(self, account_id):
		try:
			response = self.wowspy.player_personal_data(region=Region.AS, account_id=account_id, fields='statistics.pvp.battles')
			if not response:
				return -1
			elif response['status'] != 'ok':
				return -1
			in_game_name = response['data'][str(account_id)]['statistics']['pvp']['battles']
			return in_game_name
		except:
			return -1


	def get_account_id(self, in_game_name):
		"""
		Get player id from in game name.
		"""
		try:
			response = self.wowspy.players(region=Region.AS, search=in_game_name, fields='account_id')
			if not response:
				return
			elif response['status'] != 'ok':
				return
			account_id = response['data'][0]['account_id']
			return account_id
		except:
			return


	def get_player_clan_tag(self, account_id):
		try:
			response = self.wowspy.player_clan_data(region=Region.AS, account_id=account_id, extra='clan')
			if not response:
				return
			elif response['status'] != 'ok':
				return
			clan_tag = response['data'][str(account_id)]['clan']['tag']
			return clan_tag
		except:
			return


	def get_ranked_season_id(self):
		try:
			response = self.wowspy.ranked_battles_seasons(region=Region.AS, fields='season_id')
			if not response:
				return
			elif response['status'] != 'ok':
				return
			seasons = [int(value) for value in response['data'].keys() if int(value) < 100]
			return max(seasons)			
		except:
			return


	def get_rank(self, account_id, season_id):
		try:
			url = f'https://api.worldofwarships.asia/wows/seasons/accountinfo/?application_id={self.key}&season_id={season_id}&account_id={account_id}'
			response = requests.get(url).text
			if not response:
				return
			response = json.loads(response)
			if response['status'] != 'ok':
				return
			season = response['data'][str(account_id)]['seasons'][str(season_id)]
			rank = season['rank_info']['rank']
			return rank
		except:
			return
