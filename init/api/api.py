"""
Api class ONLY FOR GAMEPARAMETER PURPOSES!
Not for general api use.
"""
import json
import os
import time

import requests
from dotenv import load_dotenv

env_path = '.env'
load_dotenv(dotenv_path=env_path)
key = os.getenv('WOWS_APPLICATION_ID')


class Api:
	def __init__(self):
		self._base = 'https://api.worldofwarships.asia/wows/encyclopedia/ships/?application_id={}&fields={}&language=en&page_no={}'

	def get_ship_id_str_pages(self):
		"""
		Get how many ship_id_str pages you need to fetch.
		
		Returns
		-------
		pages : int
		"""
		time.sleep(0.1)
		result = requests.get(self._base.format(key, 'ship_id_str', 1))
		if result.status_code != 200: return
		text = result.text
		temp = json.loads(text)
		if temp['status'] != 'ok': return
		pages = temp['meta']['page_total']
		return pages


	def fetch_ship_info(self, page:int):
		"""
		Get ship_ids_str and ship_ids from api as list.
		
		Returns
		-------
		data : list
			{'id':100, 'id_str':'PJ10', 'name':'Montana', 'img':b'010101'}, ...
		"""
		time.sleep(0.1)
		result = requests.get(self._base.format(key, 'ship_id_str,images.large,name', page))
		if result.status_code != 200: return
		text = result.text
		temp = json.loads(text)
		if temp['status'] != 'ok': return
		data = []
		for k, v in temp['data'].items():
			# get binary image file
			r = requests.get(v['images']['large']).content
			if not r:
				raise Exception
			data.append(
				{'id': k,
				'id_str': v['ship_id_str'],
				'name':v['name'],
				'img':r,
				'img_final':None
				}
			)
		return data


	def fetch_maps(self):
		"""
		Get dict of map names and images from api as list.

		Returns
		-------
		d : dict
			dict of map name and image.
			{'Ocean':b'0011011', ...}
		"""
		time.sleep(0.1)
		_base_url = 'https://api.worldofwarships.asia/wows/encyclopedia/battlearenas/?application_id={}&language={}'
		result = requests.get(_base_url.format(key, 'en'))
		if result.status_code != 200:return
		text = result.text
		temp = json.loads(text)
		if temp['status'] != 'ok': return
		d = {}
		# hoping there won't be more than 100 maps...
		data = temp['data']
		for value in data.values():
			name = value['name']
			icon = requests.get(value['icon']).content
			d[name] = icon
		return d