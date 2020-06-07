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
	async def param(self, ctx, *, name):
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
		#another exact match
		elif len(result) == 1:
			self.logger.info('Found exact match for a warship.')
			embed = self.embed_builder(result[0])
			await ctx.send(embed=embed)
		elif not result:
			self.logger.debug('No result found.')
			await ctx.send('そんなもんねーよ！あ、日本艦は漢字で書いてね♡')
			return
		else:
			self.logger.info('Found multiple matches.')
			name_list = map(lambda ship:ship.name, result)
			mes = 'いっぱいヒットしちゃったよ～\n' \
				'```' + ', '.join(name_list) + '```'
			await ctx.send(mes)

	def embed_builder(self, warship:Warship):
		description = {}
		engines = []
		hulls = []
		artilleries = []
		torpedoes = []
		fire_controls = []
		shells = {}
		concealment = {}
		mobility = {}

		d = warship.to_dict()
		description['name'] = d['name']
		description['tier'] = d['tier']
		description['nation'] = d['nation'][:2]
		description['shiptype'] = d['shiptype']

		modules = ast.literal_eval(d['modules'])
		# if modules field found
		if modules is not None:
			# moduletype e.g. hull, module_ids e.g. [], [1, 2, 3]
			for module_ids in modules.values():
				# skip if no modules found
				if not module_ids:
					continue
				for module_id in module_ids:
					ship_module = self.wowsdb.get_module(module_id)
					temp = ship_module.profile
					profile = ast.literal_eval(temp)
					# key e.g. 'engine', value e.g. {...}
					for key, value in profile.items():
						if key == 'engine':
							max_speed = value['max_speed']
							engines.append(max_speed)
						elif key == 'torpedo_bomber':
							pass
						elif key == 'fighter':
							pass
						elif key == 'hull':
							aa_barrels = value['anti_aircraft_barrels']
							torp_barrels = value['torpedoes_barrels']
							health = value['health']
							planes = value['planes_amount']
							artillery_barrels = value['artillery_barrels']
							atba_barrels = value['atba_barrels']
							hulls.append({
								'aa_barrels':aa_barrels,
								'torp_barrels':torp_barrels,
								'health':health,
								'planes':planes,
								'atba_barrels':atba_barrels
							})
						elif key == 'artillery':
							rotation_time = value['rotation_time']
							max_ap = value['max_damage_AP']
							max_he = value['max_damage_HE']
							rate = value['gun_rate']
							artilleries.append({
								'rotation_time':rotation_time,
								'max_ap':max_ap,
								'max_he':max_he,
								'rate':rate
							})
						elif key == 'torpedoes':
							torp_speed = value['torpedo_speed']
							shot_speed = value['shot_speed']
							max_damage = value['max_damage']
							distance = value['distance']
							torpedoes.append({
								'speed':torp_speed,
								'shot':shot_speed,
								'max_damage':max_damage,
								'distance':distance
							})
						elif key == 'fire_control':
							distance = value['distance']
							distance_increase = value['distance_increase']
							fire_controls.append({
								'distance':distance,
								'distance_increase':distance_increase
							})
						elif key == 'flight_control':
							pass 
						elif key == 'dive_bomber':
							pass
						else:
							self.logger.critical('Unknown profile found.')

		s = self.wowsdb.get_shipparam(warship.ship_id)
		s = s.to_dict()

		mobility = ast.literal_eval(s['mobility'])
		if mobility is not None:
			rudder_time = mobility['rudder_time']
			turning_radius = mobility['turning_radius']
			max_speed = mobility['max_speed']
			mobility['rudder_time'] = rudder_time
			mobility['turning_radius'] = turning_radius
			mobility['max_speed'] = max_speed

		artillery = ast.literal_eval(s['artillery'])
		if artillery is not None:
			slots = artillery['slots']
			slots = slots.values()
			slots_str = ', '.join(map(lambda slot:f'{slot["guns"]}基{slot["barrels"]*slot["guns"]}門', slots))
			description['slots_str'] = slots_str
			max_dispersion = artillery['max_dispersion']
			shot_delay = artillery['shot_delay']
			shells = artillery['shells']
			for key, shell in shells.items():
				if key == 'HE':
					shells['HE'] = f'初速{shell["bullet_speed"]}ms^-1　最大{shell["damage"]}　装填{shot_delay}s　発火率{shell["burn_probability"]}%'
				else:
					shells[key] = f'初速{shell["bullet_speed"]}ms^-1　最大{shell["damage"]}　装填{shot_delay}s'

		torpedoes_eval = ast.literal_eval(s['torpedoes'])
		if torpedoes_eval is not None:
			visibility_dist = torpedoes_eval['visibility_dist']
			description['torp_visibility'] = visibility_dist

		concealment = ast.literal_eval(s['concealment'])
		if concealment is not None:
			detect_dist_plane = concealment['detect_distance_by_plane']
			detect_dist_ship = concealment['detect_distance_by_ship']
			if description['tier'] < 8:
				best_concealment_ship = detect_dist_ship * 0.9 * 0.97
				best_concealment_plane = detect_dist_plane * 0.9 * 0.97
			else:
				best_concealment_ship = detect_dist_ship * 0.9 * 0.9 * 0.97
				best_concealment_plane = detect_dist_plane * 0.9 * 0.9 * 0.97

			description['detect_dist_plane'] = round(detect_dist_plane, 2)
			description['best_concealment_plane'] = round(best_concealment_plane, 2)
			description['detect_dist_ship'] = round(detect_dist_ship, 2)
			description['best_concealment_ship'] = round(best_concealment_ship, 2)
	
		##################
		# CREATING EMBED #
		##################
		self.logger.debug('Creating embed.')
		embed = Embed(colour=0x793DB6, title=d['name'],
				description=f'T{d["tier"]} {d["nation"].upper()} {d["shiptype"]}')
		a = embed.add_field

		if hulls:
			for hull in hulls:
				a(name='船体', value=f'体力 {hull["health"]} ({hull["health"]+350*description["tier"]})')
				a(name='主砲', value=f'{description["slots_str"]}')
				values = ''
				if hull['atba_barrels'] != 0:
					values += f'副砲{hull["atba_barrels"]}基　'
				if hull['torp_barrels'] != 0:
						values += f'魚雷{hull["torp_barrels"]}基　'
				if hull['aa_barrels'] != 0:
					values += f'対空砲{hull["aa_barrels"]}基'
				a(name='副兵装', value=values)
				
		a(name='隠蔽', value=f'最良艦艇{description["best_concealment_ship"]}km　素{description["detect_dist_ship"]}km　' \
			f'最良航空{description["best_concealment_plane"]}km　素{description["detect_dist_plane"]}km', inline=False)		
			
		# if artilleries:
		# 	for artillery in artilleries:
		# 		# both ap and he
		# 		if artillery['max_ap'] != 0 and artillery['max_he'] != 0:
		# 			values = f'AP最大 {artillery["max_ap"]}　HE最大 {artillery["max_he"]}　180度旋回{artillery["rotation_time"]}s　装填{round(60/artillery["rate"], 1)}s'
		# 		# ships only ap
		# 		elif artillery['max_he'] == 0 and artillery['max_ap'] != 0:
		# 			values = f'AP最大 {artillery["max_ap"]}　180度旋回{artillery["rotation_time"]}s　装填{round(60/artillery["rate"], 1)}s'
		# 		# ships only he
		# 		elif artillery['max_ap'] == 0 and artillery['max_he'] != 0:
		# 			values = f'HE最大 {artillery["max_he"]}　180度旋回{artillery["rotation_time"]}s　装填{round(60/artillery["rate"], 1)}s'
		# 		else:
		# 			pass
		# 		a(name='砲弾', value=values, inline=False)
		for key, value in shells.items():
			a(name=key, value=value, inline=False)
				

		if torpedoes:
			for torp in torpedoes:
				values = f'最大{torp["max_damage"]}　' \
					f'雷速{torp["speed"]}kts　射程{torp["distance"]}km　装填{round(60 / torp["shot"], 1)}s'
				a(name='魚雷', value=values, inline=False)
		if fire_controls:
			for fire_control in fire_controls:
				values = f'射程{fire_control["distance"]}km　射程向上(?){fire_control["distance_increase"]}'
				a(name='射撃管制', value=values, inline=False)

		if engines:
			for engine in engines:
				values = f'最大速度{engine}kts'
				a(name='主機', value=values)
		values = f'転舵時間{mobility["rudder_time"]}s　転舵半径{mobility["turning_radius"]}m'
		a(name='機動性', value=values, inline=False)

		return embed
