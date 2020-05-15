

class ShipParam:
	def __init__(self, params):
		self.engine = str(params['engine'])
		self.anti_aircraft = str(params['anti_aircraft'])
		self.mobility = str(params['mobility'])
		self.hull = str(params['hull'])
		self.atbas = str(params['atbas'])
		self.artillery = str(params['artillery'])
		self.torpedoes = str(params['torpedoes'])
		self.fighters = str(params['fighters'])
		self.ship_id = params['ship_id']
		self.fire_control = str(params['fire_control'])
		self.weaponry = str(params['weaponry'])
		# self.battle_level_range_max
		# self.battle_level_range_min
		self.flight_control = str(params['flight_control'])
		self.concealment = str(params['concealment'])
		self.armour = str(params['armour'])
		self.dive_bomber = str(params['dive_bomber'])

	def __eq__(self, obj):
		return isinstance(obj, ShipParam) and self.to_tuple() == obj.to_tuple()

	def __ne__(self, obj):
		return not self == obj

	def to_tuple(self):
		params_tuple = (self.engine, self.anti_aircraft, self.mobility, self.hull, self.atbas,
			self.artillery, self.torpedoes, self.fighters, self.ship_id, self.fire_control, self.weaponry,
			self.flight_control, self.concealment, self.armour, self.dive_bomber)
		return params_tuple

	def to_dict(self):
		params_dict = {'engine':self.engine,
			'anti_aircraft':self.anti_aircraft,
			'mobility':self.mobility,
			'hull':self.hull,
			'atbas':self.atbas,
			'artillery':self.artillery,
			'torpedoes':self.torpedoes,
			'fighters':self.fighters,
			'ship_id':self.ship_id,
			'fire_control':self.fire_control,
			'weaponry':self.weaponry,
			'flight_control':self.flight_control,
			'concealment':self.concealment,
			'armour':self.armour,
			'dive_bomber':self.dive_bomber
		}
		return params_dict
	
	@staticmethod
	def shipparam_from_tuple(data:tuple):
		"""
		Convert shipparam tuple to Shipparam instance.
		"""
		if data is None:
			return None
		params_dict = {'engine':data[0],
			'anti_aircraft':data[1],
			'mobility':data[2],
			'hull':data[3],
			'atbas':data[4],
			'artillery':data[5],
			'torpedoes':data[6],
			'fighters':data[7],
			'ship_id':data[8],
			'fire_control':data[9],
			'weaponry':data[10],
			'flight_control':data[11],
			'concealment':data[12],
			'armour':data[13],
			'dive_bomber':data[14]
		}	
		sp = ShipParam(params_dict)
		return sp

	@staticmethod
	def shipparam_from_dict(data:dict):
		"""
		Convert shipparam dict to Shipparam instance.
		"""
		sp = ShipParam(data)
		return sp