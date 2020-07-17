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
		for key, value in params.items():
			try:
				module = get_module_type(key, value)
				if module is None:
					continue
				kv = {key:value}
				if module == 'A':
					a.append(kv)
				elif module == 'E':
					e.append(kv)
				elif module == 'FC':
					fc.append(kv)
				elif module == 'H':
					h.append(kv)
				elif module == 'T':
					t.append(kv)
			except:
				pass
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

def get_module_type(key, value:dict):
	if 'Artillery' in key:
		return 'A'
	elif 'Engine' in key:
		return 'E'
	elif 'FireControl' in key:
		return 'FC'
	elif 'Hull' in key:
		return 'H'
	elif 'Torpedoes' in key:
		return 'T'
	if not isinstance(value, dict):
		return None
	for k, v in value.items():
		if not isinstance(v, dict):
			continue
		try:
			if v['typeinfo']['species'] == 'Main':
				return 'A'
			elif v['typeinfo']['species'] == 'Torpedo':
				return 'T'
		except:
			pass
	return None
			