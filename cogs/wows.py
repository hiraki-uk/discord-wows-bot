import ast
import asyncio
import datetime
import json
import math
import sqlite3
import traceback

import requests
from discord import Embed
from discord.ext import commands, tasks

from cogs.cogfunctions.database import Database
from scripts.logger import Logger
from wows.shipparam import ShipParam
from wows.warship import Warship
from wows.wowsdb import Wows_database


db_path = 'wows.db'


class WowsCog(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
		self.logger = Logger(self.__class__.__name__)
		self.wowsdb = Wows_database(db_path)

	@commands.command()
	async def param(self, ctx, name=None):
		"""
		そのぽふねのデータ教えてあげる！
		"""
		self.logger.info('Recieved param command.')
		if name is None:
			await ctx.send('どのぽふねのデータがほしいの？\n日本艦は漢字で登録されてるから気を付けて！')
			return
		result = self.wowsdb.get_warship(name)
		# exact match
		if isinstance(result, Warship):
			self.logger.info('Found exact match for a warship.')
			embed = self.embed_builder(result)
			await ctx.send(embed=embed)
		elif result is None:
			self.logger.debug('No result found.')
			await ctx.send('そんなもんねーよ！あ、日本艦は漢字で書いてね♡')
			return
		else:
			self.logger.info('Found multiple match for a warship.')
			name_list = list(map(lambda ship:ship.name, result))
			mes = 'いっぱいヒットしちゃったよ～\n' \
				'```' + str(name_list) + '```'
			await ctx.send(mes)

	def embed_builder(self, warship:Warship):
		self.logger.debug('Creating embed.')

		d = warship.to_dict()
		name = d['name']
		tier = d['tier']
		nation = d['nation'][:2]
		shiptype = d['shiptype']
		embed = Embed(colour=0x793DB6, title=d['name'], description=f'T{tier} {nation.upper()} {shiptype}')
		a = embed.add_field

		s = self.wowsdb.get_shipparam(warship.ship_id)
		s = s.to_dict()

		mobility = ast.literal_eval(s['mobility'])
		if mobility is not None:
			rudder_time = mobility['rudder_time']
			turning_radius = mobility['turning_radius']
			max_speed = mobility['max_speed']
			a(name='機動性', value=f'{max_speed}kts　転舵時間{rudder_time}s　転舵半径{turning_radius}m', inline=False)

		hull = ast.literal_eval(s['hull'])
		if hull is not None:
			torp_barrels = hull['torpedoes_barrels']
			health = hull['health']
			artillery_barrels = hull['artillery_barrels']
			if torp_barrels == 0:
				a(name='船体性能', value=f'体力{health}　主砲{artillery_barrels}基', inline=False)
			else:
				a(name='船体性能', value=f'体力{health}　主砲{artillery_barrels}基　魚雷{torp_barrels}基', inline=False)

		artillery = ast.literal_eval(s['artillery'])
		if artillery is not None:
			max_dispersion = artillery['max_dispersion']
			shot_delay = artillery['shot_delay']
			shells = artillery['shells']
			for key, shell in shells.items():
				if key == 'HE':
					a(name=f'{key}', value=f'{shell["bullet_speed"]}ms^-1　最大{shell["damage"]}　装填{shot_delay}s　発火率{shell["burn_probability"]}%', inline=False)
				else:
					a(name=f'{key}', value=f'{shell["bullet_speed"]}ms^-1　最大{shell["damage"]}　装填{shot_delay}s', inline=False)
				
		torpedoes = ast.literal_eval(s['torpedoes'])
		if torpedoes is not None:
			visibility_dist = torpedoes['visibility_dist']
			distance = torpedoes['distance']
			reload_time = torpedoes['reload_time']
			torp_speed = torpedoes['torpedo_speed']
			max_damage = torpedoes['max_damage']
			a(name='魚雷性能', value=f'被発見{visibility_dist}km　装填{reload_time}s　雷速{torp_speed}kts^-1　最大{max_damage}', inline=False)

		fire_control = ast.literal_eval(s['fire_control'])
		if fire_control is not None:
			distance = fire_control['distance']
			distance_increase = fire_control['distance_increase']
			a(name='射程', value=f'{distance}km　distance_increaseﾅﾆｺﾚ{distance_increase}', inline=False)

		concealment = ast.literal_eval(s['concealment'])
		if concealment is not None:
			detect_dist_plane = concealment['detect_distance_by_plane']
			detect_dist_ship = concealment['detect_distance_by_ship']
			if tier < 8:
				best_concealment = detect_dist_ship * 0.9 * 0.97
			else:
				best_concealment = detect_dist_ship * 0.9 * 0.9 * 0.97
			best_concealment = round(best_concealment, 2)
			a(name='隠蔽性', value=f'航空発見{detect_dist_plane}km　艦艇発見{detect_dist_ship}km　最良{best_concealment}km（誤差有）', inline=False)

		del a
		return embed
