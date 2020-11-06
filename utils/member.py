class Member:
	def __init__(self, **kwargs) -> None:
		self.kwargs = kwargs
		

	def to_dict(self):
		return self.kwargs


	def account_id(self):
		account_id = self.kwargs.get('account_id')
		return account_id


	def discord_id(self):
		discord_id = self.kwargs.get('discord_id')
		return discord_id


	def battles(self):
		weekly_battles = self.kwargs.get('battles')
		if not weekly_battles:
			return 0
		return weekly_battles 


	def set_battles(self, battles):
		temp = {'battles':battles}
		self.kwargs.update(temp)


	def set_value(self, key, value):
		temp = {key:value}
		self.kwargs.update(temp)
		return True


if __name__ == '__main__':
	member = Member(hello=1, world=2)
	print(member.to_dict())
	print(member.kwargs)