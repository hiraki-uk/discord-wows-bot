import json

import requests

from scripts.logger import Logger
from wows.module import ShipModule
from wows.shipparam import ShipParam
from wows.warship import Warship


class WowsApi:
	def __init__(self, application_id):
		self.application_id = application_id
		self.logger = Logger(self.__class__.__name__)

	def get_module(self, module_id):
		"""
		Get the module data of a given module id.
		"""
		self.logger.debug(f'Fetching module data for {module_id}.')
		response = requests.get('https://api.worldofwarships.asia/wows/encyclopedia/modules/?' \
			f'application_id={self.application_id}&module_id={module_id}&language=en')
		if response.status_code != 200:
			self.logger.critical('Invalid status code.')
			return
		text = response.text
		text_json = json.loads(text)
		if text_json['status'] != 'ok':
			self.logger.critical('Invalid status code.')
			return
		data = text_json['data'][str(module_id)]
		shipmodule = ShipModule.module_from_dict(data)
		return shipmodule
		
	def get_warships_count(self):
		"""
		Get the number of warships registered in wows API.
		"""
		self.logger.debug('Counting warships.')
		response = requests.get('https://api.worldofwarships.asia/wows/encyclopedia/ships/?' \
			f'application_id={self.application_id}&limit=1&language=en')
		if response.status_code != 200:
			self.logger.critical('Invalid status code.')
			return
		text = response.text
		text_json = json.loads(text)
		if text_json['status'] != 'ok':
			self.logger.critical('Invalid status.')
			return
		warships_count = text_json['meta']['total']
		self.logger.debug(f'Found {warships_count} ships.')
		return warships_count

	def get_warships(self, pages):
		"""
		Get list of warships as list of Warship instance.
		"""
		self.logger.debug(f'Getting warships for {pages} pages.')
		warship_list = []
		for i in range(pages):
			response = requests.get('https://api.worldofwarships.asia/wows/encyclopedia/ships/?' \
				f'application_id={self.application_id}&page_no={i+1}&language=en')
			if response.status_code != 200:
				self.logger.critical('Invalid status code.')
				return
			text = response.text
			text_json = json.loads(text)
			if text_json['status'] != 'ok':
				self.logger.critical('Invalid status code.')
				return
			values = text_json['data'].values()
			for v in values:
				temp = Warship.warship_from_dict(v)
				warship_list.append(temp)
		self.logger.debug(f'Created {len(warship_list)} warships.')
		return warship_list

	def get_ship_profile(self, ship_id):
		"""
		Get ShipParam instance of given ship id.
		"""
		response = requests.get('https://api.worldofwarships.asia/wows/encyclopedia/shipprofile/?' \
			f'application_id={self.application_id}&ship_id={ship_id}&language=en')
		if response.status_code != 200:
			self.logger.critical('Invalid status code.')
			return
		text = response.text
		text_json = json.loads(text)
		if text_json['status'] != 'ok':
			self.logger.debug('Invalid status code.')
			return
		param = text_json['data'][str(ship_id)]
		shipparam = ShipParam.shipparam_from_dict(param)
		return shipparam
		
	def information_about_encyclopedia(self):
		"""
		Get when encyclopedia was last updated.
		"""
		self.logger.debug('Fetching last ships_updated_at.')
		response = requests.get('https://api.worldofwarships.asia/wows/encyclopedia/info/?' \
			f'application_id={self.application_id}&fields=ships_updated_at&language=en')
		if response.status_code != 200:
			self.logger.critical('Invalid status code.')
			return
		text = response.text
		text_json = json.loads(text)
		if text_json['status'] != 'ok':
			self.logger.debug('Invalid status code.')
			return
		version = text_json['data']['ships_updated_at']
		self.logger.debug(f'Encyclopedia was last updated at {version}.')
		return version
