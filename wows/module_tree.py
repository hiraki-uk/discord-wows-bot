from wows.module import ShipModule
from wows.wowsdb import Wows_database


class Module_node:
	def __init__(self, module_id:int, next_ids:list, next_nodes=None):
		self.module_id = module_id
		self.next_ids = next_ids		
		self.next_nodes = next_nodes


class Module_tree:
	def _init__(self, data:dict, wowsdb:Wows_database):
		defaults = []
		for key, module in data:
			if module['is_default'] is True:
				defaults.append(module)
				data.pop(key)
		self.torp = None
		self.suo = None
		self.engine = None
		self.hull = None
		self.artillery = None
		self.engine = None
		for module in defaults:
			if module['type'] == 'Torpedoes':
				self.torp = Module_node(module['module_id'], module['next_modules'])
				self.torp.next_nodes = list(
					map(
						lambda module_id:Module_node(
							module_id, 
							data[str(module_id)]
						),
						module['next_modules']
					)
				)
			elif module['type'] == 'Suo':
				self.suo = Module_node(module['module_id'], module['next_modules'])
				self.torp.next_nodes = list(map(
					lambda module_id:Module_node(
						module_id, 
						data[str(module_id)]
					),
					module['next_modules']
				))
			elif module['type'] == 'Hull':
				self.hull = Module_node(module['module_id'], module['next_modules'])
				self.torp.next_nodes = list(map(
					lambda module_id:Module_node(
						module_id, 
						data[str(module_id)]
					),
					module['next_modules']
				))
			elif module['type'] == 'Artillery':
				self.artillery = Module_node(module['module_id'], module['next_modules'])
				self.torp.next_nodes = list(map(
					lambda module_id:Module_node(
						module_id, 
						data[str(module_id)]
					),
					module['next_modules']
				))
			elif module['type'] == 'Engine':
				self.engine = Module_node(module['module_id'], module['next_modules'])
				self.torp.next_nodes = list(map(
					lambda module_id:Module_node(
						module_id, 
						data[str(module_id)]
					),
					module['next_modules']
				))
		# get the root 
		temp = self.torp
		