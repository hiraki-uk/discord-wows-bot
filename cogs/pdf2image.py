import os

from config.config import get_config
from discord.ext import commands

from pdf2image import convert_from_bytes


# poppler/binを環境変数PATHに追加する
poppler_dir = get_config().get('poppler_bin')
os.environ["PATH"] += os.pathsep + str(poppler_dir)

class Pdf2Image(commands.Cog):
	"""	pdfを写真に変換するよ! """

	def __init__(self, mitsuba):
		self.bot = mitsuba.bot
  
	@commands.command()
	async def pdf2jpeg(self, ctx):
		""" pdfをjpegに変換するよ """
		attachments = ctx.message.attachments

		if not attachments:
			await ctx.send('pdfないじゃん!')
			return

		try:
			for attachment in attachments:
				binary = await attachment.read()
				pages = convert_from_bytes(binary)
				for i, page in enumerate(pages):
					page
		except Exception as e:
			await ctx.send('えらったｗ')
			return

		# await ctx.send('```' + f.read() + '```')
			