import discord
from discord.ext import commands, tasks

from scripts.logger import Logger
import json

	
"""
Responsible for managing member.json file.
"""

class MembersManager:
	def __init__(self, members):
		self.logger = Logger(__name__)
		# initialize file if empty
		with open('members.json', 'r') as f:
			temp = f.read()
		if not temp:
			self._init_file(members)

	def _init_file(self, members:dict):
		"""
		Initialize members.json file with members.
		"""
		with open('members.json', 'w') as f:
			f.write(json.dumps(members, indent=4))

	def is_registered(self, discord_id:int):
		"""
		Check if given discord id is registered.
		"""
		members = registered_members()
		if not members:
			self.logger.debug('No member found.')
			return False
		for member in members:
			if discord_id == member['discord_id']:
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
				return None
			members = json.loads(temp)
		return members

	def register(self, member):
		"""
		Register member into member.json.
		"""
		if not member.get('discord_id'):
			self.logger.debug('Member does not contain discord_id.')
			return
		with open('members.json', 'r') as f:
			temp = f.read()
			if not temp:
				self.logger.debug('members.json is empty.')
				members = []
			else:
				members = json.loads(temp)
		
		members.append(member)
		with open('members.json', 'w') as f:
			f.write(json.dumps(members, indent=4))

	def update(self):
		"""
		Update member's information.
		"""
		pass

	def update_members(self, members:list):
		"""
		Update members' information.
		"""
		# read member.json
		with open('members.json', 'r') as f:
			temp = f.read()
		if not temp:
			members_old = {}
		else:
			members_old = json.loads(temp)
		
		# update members_old
		for member in members_old:
			discord_id = member['discord_id']
		with open('members.json', 'w') as f:
			f.write(json.dumps(members, indent=4))
