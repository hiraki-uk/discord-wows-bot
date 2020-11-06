import json
import os
import re

from bs4 import BeautifulSoup, ResultSet, Tag
from dotenv import load_dotenv
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from utils.exceptions import ScrapingException

load_dotenv(dotenv_path='.env')
exe_path = os.getenv('EXECUTABLE_PATH')


class Homepage_Scraper:
	__slots__ = ('debug',)
	
	def __init__(self, debug=False):
		self.debug = debug


	def scrape_wowshp(self) -> bytes:
		"""
		Scrapes wows hp and returns its source.

		Returns
		-------
		source : bytes
			wows hp source in bytes
		"""
		options = Options()
		options.headless = True
		options.add_experimental_option('excludeSwitches', ['enable-logging'])
		if exe_path:
			driver = Chrome(executable_path="database/chromedriver.exe", options=options)
		else:
			driver = Chrome(options=options)
		driver.get('https://worldofwarships.asia/ja/')
		source = driver.page_source.encode('utf-8')
		driver.quit()
		return source
	

	def get_main(self, source) -> Tag:
		"""
		Get main tag from a given source.
		"""
		soup = BeautifulSoup(source, 'html.parser')
		main = soup.main
		if self.debug:
			with open('hp.html', 'w', encoding='utf-8') as f:
				f.write(str(main))
		return main


	def get_alart_div(self, main: Tag) -> Tag:
		""" 
		Find and return alart information.

		Parameters
		----------
		main
			main Tag object

		Returns
		-------
		alart_div
			div Tag object with alart information 
		"""
		temp = main.find(string='重要メッセージ').parent
		alart_div = temp.parent # temporary as it is, add .parent if needed
		if self.debug:
			with open('alart_div.html', 'w', encoding='utf-8') as f:
				f.write(str(alart_div))
		return alart_div


	def get_row_div(self, main: Tag) -> Tag:
		"""
		Find and return row Tag with news information.

		Parameters
		----------
		main
			main Tag object

		Returns
		-------
		row_div
			row Tag object with news information
		
		"""
		temp = main.find('div', {'class':'news-tiles col-12'})
		row_div = temp.find('div', {'class':'row'})
		if self.debug:
			with open('news-tiles.html', 'w', encoding='utf-8') as f:
				f.write(str(temp))
			with open('row_div.html', 'w', encoding='utf-8') as f:
				f.write(str(row_div))
		return row_div


	def get_articles(self, row_div: Tag) -> ResultSet:
		"""
		From row div Tag object, return all article Tag object.

		Parameters
		----------
		row_div
			row div Tag object with news information
		
		Returns
		-------
		articles
			ResultSet objects with articles Tag objects
		"""
		articles = row_div.findAll('article')
		if self.debug:
			with open('articles.html', 'w', encoding='utf-8') as f:
				f.write(str(articles))
		return articles


	def get_article_lists(self, articles: ResultSet) -> list:
		"""
		From articles, parses and returns articles as a list.

		Parameters
		----------
		articles : ResultSet
			ResultSet object

		Returns
		-------
		article_list : list
			processed articles as a list
		"""
		article_list = []
		for article in articles:
			try:
				skew_title = str(article.find('div', {'class':'skew__title'}).span.string)
			except:
				skew_title = None
			img = str(article.find('div', {'class':'_img'})['style'].split('url')[1])
			img = re.search(r'\((.+?\))', img).group(0)
			img = img[2:-2]
			title = str(article.find('h3', {'class':{'tile__title'}}).string)
			try:
				# title_description = str(article.find('span', {'class':'tile__description'}).string).strip(' ', '　')
				title_description = article.find('span', {'class':'tile__description'}).string.strip()
			except:
				title_description = None
			try:
				url = 'https://worldofwarships.asia' + article.find('a', {'class':'fit-link'})['href']
			except:
				url = None
			temp = ('wowshomepage', title, title_description, url, img)
			article_list.append(temp)
		if self.debug:
			with open('article_list.json', 'w', encoding='utf-8') as f:
				f.write(json.dumps(article_list, indent=4, ensure_ascii=False))
		# temporary returning only one article
		article_list = [article_list[0]]
		return article_list


def get_hp_articles():
	scraper = Homepage_Scraper()
	source = scraper.scrape_wowshp()
	main = scraper.get_main(source)
	row = scraper.get_row_div(main)
	articles = scraper.get_articles(row)
	articlelist = scraper.get_article_lists(articles)
	# sometimes getposts does not work
	if not articlelist:
		raise ScrapingException('Unable to scrape articles.')
	return articlelist


if __name__ == '__main__':
	print(get_hp_articles())
