

class ShipModule:
	def __init__(self, data):
		self.name = data['name']
		self.image = data['image']
		self.tag = data['tag']
		self.module_id_str = data['module_id_str']
		self.module_id = data['module_id']
		try:
			self.moduletype = data['type']
		except KeyError:
			self.moduletype = data['moduletype']
		self.price_credit = data['price_credit']
		self.profile = data['profile']

		# override above data
		self.profile = str(self.profile)
		
	def __eq__(self, obj):
		return isinstance(obj, ShipModule) and self.to_tuple() == obj.to_tuple()

	def __ne__(self, obj):
		return not self == obj

	def to_tuple(self):
		module_tuple = (
			self.name, self.image, self.tag, self.module_id_str, self.module_id,
			self.moduletype, self.price_credit, self.profile
		)
		return module_tuple
	
	def to_dict(self):
		module_dict = {
			'name': self.name, 'image': self.image, 'tag': self.tag, 'module_id_str': self.module_id_str, 'module_id': self.module_id,
			'moduletype': self.moduletype, 'price_credit': self.price_credit, 'profile': self.profile
		}
		return module_dict

	@staticmethod
	def module_from_tuple(data:tuple):
		"""
		Create module instance from tuple.
		"""
		if data is None:
			return None
		module_dict = {
			'name': data[0], 
			'image': data[1], 
			'tag': data[2], 
			'module_id_str': data[3], 
			'module_id': data[4],
			'moduletype': data[5], 
			'price_credit': data[6], 
			'profile': data[7]
		}
		ship_module = ShipModule(module_dict)
		return ship_module
		
	@staticmethod
	def module_from_dict(data:dict):
		"""
		Create module instance from dict.
		"""
		ship_module = ShipModule(data)
		return ship_module