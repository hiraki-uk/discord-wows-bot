import json


class Warship:
	def __init__(self, d:dict):
		self.name = d['name']
		self.index = d['index']
		self.shipid = d['id']
		self.tier = d['tier']
		self.species = d['species']
		self.nation = d['nation']

		self.mods = d['mods']
		self.artilleries = d['artilleries']
		self.engines = d['engines']
		self.firecontrols = d['firecontrols']
		self.hulls = d['hulls']
		self.torpedoes = d['torpedoes']


	@classmethod
	def from_tuple(cls, t:tuple):
		"""
		Creates warship instance from tuple.
		Use for creating warship instance from result in  warship database.
		"""
		d = {
			'name': t[0],
			'index': t[1],
			'id': t[2],
			'tier': t[3],
			'species': t[4],
			'nation': t[5],
			'mods': json.loads(t[6]),
			'artilleries': json.loads(t[7]),
			'engines': json.loads(t[8]),
			'firecontrols': json.loads(t[9]),
			'hulls': json.loads(t[10]),
			'torpedoes': json.loads(t[11])
		}
		return cls(d)


	@classmethod
	def from_params(cls, gpm, params:dict):
		"""
		Creates warship instance of given parameters.
		Use for creating warship instance from result in gameparams database.
		"""
		# description extracted outside each module
		name = params['name']
		index = params['index']
		shipid = params['id']
		tier = params['level']
		typeinfo = params['typeinfo']
		species = typeinfo['species']
		nation = typeinfo['nation']

		mods = [
			[],
			[],
			[],
			[],
			[],
			[]
		]
		a = []
		e = []
		fc = []
		h = []
		t = []

		# get all mods
		all_mods = gpm.get_all_mods()
		# check eligibility
		for mod in all_mods:
			if is_eligible(name, tier, species, nation, mod):
				idx = mod.slot
				mods[idx].append(mod.simplified())
			
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
		artilleries = []
		engines = []
		firecontrols = []
		hulls = []
		torpedoes = []
		for artillery in a:
			temp = create_artillery_description(artillery, gpm)
			artilleries.append(temp)

		for engine in e:
			temp = create_engine_description(engine)
			engines.append(temp)

		for firecontrol in fc:
			temp = create_fc_description(firecontrol)
			firecontrols.append(temp)

		for hull in h:
			temp = create_hull_description(hull)
			hulls.append(temp)
		for torp in t:
			temp = create_torp_description(torp, gpm)
			torpedoes.append(temp)
		d = {
			'name': name,
			'index': index,
			'id': shipid,
			'tier': tier,
			'species': species,
			'nation': nation,

			'mods': mods,
			'artilleries': artilleries,
			'engines': engines,
			'firecontrols': firecontrols,
			'hulls': hulls,
			'torpedoes': torpedoes,		
		}
		warship = cls(d)
		return warship


	def to_dict(self):
		d = {
			'name': self.name,
			'index': self.index,
			'id': self.shipid,
			'tier': self.tier,
			'species': self.species,
			'nation': self.nation,

			'mods': self.mods,
			'artilleries': self.artilleries,
			'engines': self.engines,
			'firecontrols': self.firecontrols,
			'hulls': self.hulls,
			'torpedoes': self.torpedoes,		
		}
		return d


def is_eligible(name, tier, species, nation, mod):
	"""
	Checks if the instance is eligible to
	use the module.
	"""
	# if shipname specified, true
	if name in mod.ships:
		return True
	# tier eligibility
	if tier not in mod.shiplevel:
		return False
	# shiptype eligibility
	if species not in mod.shiptype:
		return False
	# nation eligibility
	if nation not in mod.nation:
		return False
	# excludes
	if name in mod.excludes:
		return False
	# rest are eligible
	return True


def create_artillery_description(a, gpm):
	a = list(a.values())[0]
	# find main guns
	guns = []
	ammolist = []
	for value in a.values():
		try:
			if value['typeinfo']['type'] == 'Gun':
				# check ammunition
				for ammo in value['ammoList']:
					if ammo not in ammolist: ammolist.append(ammo)
				guns.append({
				'barrelDiameter': value['barrelDiameter'],
				'numBarrels': value['numBarrels'],
				'rotationSpeed':round(180/value['rotationSpeed'][0]),
				'shotDelay': value['shotDelay'],
				})
		except Exception as e:
			pass
	# create ammo
	ammolist = [gpm.search_artillery(ammo).to_dict() for ammo in ammolist]

	artillery = {
		'maxDist': a['maxDist'],
		'sigma': a['sigmaCount'],
		'minDistH': a['minDistH'],
		'minDistV': a['minDistV'],
		'normalDistribution': a['normalDistribution'],
		'ammolist': ammolist,
		'guns': guns
	}
	return artillery


def create_engine_description(e):
	pass


def create_fc_description(fc):
	fc = list(fc.values())[0]
	return fc['maxDistCoef']


def create_hull_description(h):
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


def create_torp_description(t, gpm):
	t = list(t.values())[0]
	guns = []
	for key, value in t.items():
		try:
			if value['typeinfo']['type'] == 'Gun':
				ammolist = value['ammoList']
				torp_list = []
				for ammo in ammolist:
					torp = gpm.search_torp(ammo)
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