import io
import json

from discord import Embed, File
from discord.ext import commands
from utils.logger import Logger

from wows.wowsapi import WowsApi
from wows.gameparams_manager import GP_Manager


class WowsCog(commands.Cog):
	def __init__(self, bot, wows_application_id):
		self.bot = bot
		self.logger = Logger(self.__class__.__name__)
		self.wows = GP_Manager()
		self.api = WowsApi(wows_application_id)


	@commands.command(aliases=['param'])
	async def pm(self, ctx, *, name=None):
		"""
		そのぽふねのデータ教えてあげる！
		"""
		self.logger.info('Recieved param command.')
		if name is None:
			await ctx.send('どのぽふねのデータがほしいの？ うむらると？諦めろ')
			return
		result = self.wows.search_ship_id_str(name)
		if not result:
			self.logger.debug('No result found.')
			await ctx.send('誰よその女！')
			return
		# exact match
		elif isinstance(result, str):
			self.logger.info('Found exact match for a warship.')
			embed = self.embed_builder(result, False)
			await ctx.send(embed=embed)
		else:
			self.logger.info('Found multiple matches.')
			mes = 'いっぱいヒットしちゃったよ～　艦名の日本語のところは除いて教えてね\n' \
				'```' + ', '.join(result) + '```'
			await ctx.send(mes)


	@commands.command()
	async def pmv(self, ctx, *, name=None):
		"""
		そのぽふねのデータ教えてあげる！
		"""
		self.logger.info('Recieved param command.')
		if name is None:
			await ctx.send('どのぽふねのデータがほしいの？ うむらると？諦めろ')
			return
		result = self.wows.search_ship_id_str(name)
		if not result:
			self.logger.debug('No result found.')
			await ctx.send('誰よその女！')
			return
		# exact match
		elif isinstance(result, str):
			self.logger.info('Found exact match for a warship.')
			embed = self.embed_builder(result, True)
			temp = File(io.StringIO(json.dumps(embed, indent=4)), filename='params.json')
			await ctx.send(file=temp)
		else:
			self.logger.info('Found multiple matches.')
			mes = 'いっぱいヒットしちゃったよ～　艦名の日本語のところは除いて教えてね\n' \
				'```' + ', '.join(result) + '```'
			await ctx.send(mes)


	def embed_builder(self, result, v:bool):
		"""
		Creates and returns embed.
		set show_id to True for showing ship id.

		Params
		------
		result : str
			ship_id_str of a warship.
		"""
		warship = self.wows.search_ship(result, v)
		if v:
			return warship
		embed = Embed(colour=0x793DB6, title=warship.name,
				description=f'T{warship.tier} {warship.typeinfo["nation"][:2].upper()} {warship.typeinfo["species"]},　shipID {warship.shipid}')
		a = embed.add_field
		if warship.hulls:
			for hull in warship.hulls:
				if warship.tier > 7 or \
					'Belfast' in warship.name or \
					'Z-39' in warship.name:
					best_concealment_ship = round(hull["visibility"] * 0.9 * 0.9 * 0.97, 2)
					best_concealment_plane = round(hull['visibility_plane'] * 0.9 * 0.9 * 0.97, 2)
				else:
					best_concealment_ship = round(hull["visibility"] * 0.9 * 0.97, 2)
					best_concealment_plane = round(hull['visibility_plane'] * 0.9 * 0.97, 2)

				a(name='\n船体', value=f'体力 {round(hull["health"])}　（{round(hull["health"])+350*warship.tier}）　最良隠蔽{best_concealment_ship}km　航空{best_concealment_plane}km\n' \
					f'速力{hull["max_speed"]}kts　全長{hull["size"]}m　旋回半径{hull["turning_radius"]}m', inline=False)

		if warship.artilleries:
			for artillery in warship.artilleries:
				numbarrels = 0
				rotation_speed = 0
				shotdelay = 0
				for gun in artillery['guns']:
					barrelDiameter = gun['barrelDiameter']
					numbarrels += gun['numBarrels']
					rotation_speed = gun['rotationSpeed']
					shotdelay = gun['shotDelay']
				a(name='主砲', value=f'{round(barrelDiameter*1000)}mm砲　{len(artillery["guns"])}基　{round(numbarrels)}門　装填{shotdelay}s　180度旋回{rotation_speed}s　σ{artillery["sigma"]} ' \
					f'通常散布={artillery["normalDistribution"]}', inline=False)

		if warship.torpedoes:
			for torp in warship.torpedoes:
				for gun in torp['guns']:
					torp_info = ''
					for tp in gun['torps']:
						torp_info += f'{round(tp["maxDist"], 1)}km　{tp["speed"]}kts　被発見{tp["visibility"]}km　{tp["dmg"]}dmg\n'
					break
				numbarrels = sum(map(lambda x:x['numBarrels'], torp['guns']))
				shotdelay = torp['guns'][0]['shotDelay']
				a(name='魚雷', value=f'{len(torp["guns"])}基{numbarrels}門　装填{shotdelay}s　{torp_info}', inline=False)
			
		if warship.firecontrols:
			a(name='射撃管制', value=',　'.join(list(map(
				lambda firecontrol:f'射程{round(artillery["maxDist"] * firecontrol / 1000, 2)}km',
				warship.firecontrols
			))), inline=False)
		return embed
