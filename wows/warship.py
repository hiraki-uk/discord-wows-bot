import json
from wows.module import get_torp


class Artillery:pass
class Engine:pass
class Firecontrol:pass
class Hull:pass
class Torp:pass

 
class Warship:
	def __init__(self, params:dict):
		# description extracted outside each module
		self.name = params['name']
		self.index = params['index']
		self.shipid = params['id']
		self.tier = params['level']
		self.typeinfo = params['typeinfo']
		
		a = []
		e = []
		fc = []
		h = []
		t = []
		keys = params.keys()
		for key in keys:
			kv = {key:params[key]}
			if 'Artillery' in key:
				a.append(kv)
			elif 'Engine' in key:
				e.append(kv)
			elif 'FireControl' in key:
				fc.append(kv)
			elif 'Hull' in key:
				h.append(kv)
			elif 'Torpedoes' in key:
				t.append(kv)
		a = sorted(a, key=lambda x:x.keys())	
		e = sorted(e, key=lambda x:x.keys())
		fc = sorted(fc, key=lambda x:x.keys())
		h = sorted(h, key=lambda x:x.keys())
		t = sorted(t, key=lambda x:x.keys())
		# extracting description from each module
		self.artilleries = []
		self.engines = []
		self.firecontrols = []
		self.hulls = []
		self.torpedoes = []
		for artillery in a:
			temp = create_artillery_description(artillery)
			self.artilleries.append(temp)

		for engine in e:
			temp = create_engine_description(engine)
			self.engines.append(temp)

		for firecontrol in fc:
			temp = create_fc_description(firecontrol)
			self.firecontrols.append(temp)

		for hull in h:
			temp = create_hull_description(hull)
			self.hulls.append(temp)
		for torp in t:
			temp = create_torp_description(torp)
			self.torpedoes.append(temp)

def create_artillery_description(a:Artillery):
	a = list(a.values())[0]
	# find main guns
	guns = []
	for key, value in a.items():
		try:
			if value['typeinfo']['type'] == 'Gun':
				guns.append({
				'barrelDiameter': value['barrelDiameter'],
				'numBarrels': value['numBarrels'],
				'rotationSpeed':value['rotationSpeed'][1],
				'shotDelay': value['shotDelay'],
				})
		except Exception as e:
			pass
	artillery = {
		'maxDist': a['maxDist'],
		'sigma': a['sigmaCount'],
		'minDistH': a['minDistH'],
		'minDistV': a['minDistV'],
		'normalDistribution': a['normalDistribution'],
		'guns': guns
	}
	return artillery

def create_engine_description(e:Engine):
	pass

def create_fc_description(fc:Firecontrol):
	fc = list(fc.values())[0]
	return fc['maxDistCoef']

def create_hull_description(h:Hull):
	h = list(h.values())[0]
	hull = {
		'health': h['health'],
		'max_speed': h['maxSpeed'],
		'size': h['size'][0],
		'engine_power': h['enginePower'],
		'turning_radius': h['turningRadius'],
		'visibility': h['visibilityFactor'],
		'visibility_plane': h['visibilityFactorByPlane'],
	}
	return hull

def create_torp_description(t:Torp):
	t = list(t.values())[0]
	guns = []
	for key, value in t.items():
		try:
			if value['typeinfo']['type'] == 'Gun':
				ammolist = value['ammoList']
				torp_list = []
				for ammo in ammolist:
					torp = get_torp(ammo)
					torp_list.append({
						'dmg': round(torp['alphaDamage']/(torp['damageCoeffMaxPing']+1)+torp['damage']),
						'maxDist': round(torp['maxDist']*30/1000, 2),
						'speed': torp['speed'],
						'visibility': torp['visibilityFactor']
					})
				guns.append({
				'numBarrels': value['numBarrels'],
				'shotDelay': value['shotDelay'],
				'torps': torp_list
				})
		except Exception as e:
			pass
	torp = {
		'guns': guns
	}
	return torp
