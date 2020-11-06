"""
Responsible for managing member.json file.
"""
import json
import os

from utils.logger import Logger
from utils.member import Member


class MembersManager:
	def __init__(self):
		self.logger = Logger(self.__class__.__name__)
		# create file is doesn't exist
		if not os.path.exists('members.json'):
			with open('members.json', 'w') as f:
				pass
		# if exists 
		else:
			with open('members.json', 'r') as f:
				temp = f.read()
			if not temp:
				self._init_file()


	def _init_file(self):
		"""
		Initialize members.json file.
		"""
		with open('members.json', 'w') as f:
			f.write('[]')


	def is_registered(self, discord_id:int):
		"""
		Check if given discord id is registered.
		"""
		members = self.registered_members()
		if not members:
			self.logger.debug('No member found.')
			return False
		for member in members:
			if discord_id == member.discord_id():
				self.logger.debug('Member is registered.')
				return True
		self.logger.debug('Member not registered.')
		return False


	def registered_members(self):
		"""
		Get a list of registered members.
		"""
		with open('members.json', 'r') as f:
			temp = f.read()
			if not temp:
				self.logger.debug('members.json file is empty.')
				return []
		members = [Member(**member) for member in json.loads(temp)]
		return members


	def register_member(self, member:Member):
		"""
		Register member into member.json.
		Returns True after registeration.
		"""
		if self.is_registered(member.discord_id()):
			return
		members = self.registered_members()		
		members.append(member)
		with open('members.json', 'w') as f:
			f.write(json.dumps([m.to_dict() for m in members]))
		return True


	def deregister_member(self, discord_id:int):
		if not self.is_registered(discord_id):
			return
		members_old = self.registered_members()
		members_new = [m for m in members_old if m.discord_id() != discord_id]
		with open('members.json', 'w') as f:
			f.write(json.dumps([m.to_dict() for m in members_new]))
		return True


	def update_member(self, member:Member):
		"""
		Update member's information.
		Returns True after update.
		"""
		if not self.is_registered(member.discord_id()):
			return
		old_members = self.registered_members()
		new_members = [m for m in old_members if m.discord_id() != member.discord_id()]
		with open('members.json', 'w') as f:
			f.write(json.dumps([m.to_dict() for m in new_members]))
		return True


	def update_members(self, members:list):
		"""
		Update members' information.
		Returns True after update.
		"""
		with open('members.json', 'w') as f:
			f.write(json.dumps([member.to_dict() for member in members]))
		return True
