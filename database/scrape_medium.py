import json
import os

from bs4 import BeautifulSoup, Tag
from dotenv import load_dotenv
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from utils.exceptions import ScrapingException

load_dotenv(dotenv_path='.env')
exe_path = os.getenv('EXECUTABLE_PATH')


class Medium:
	__slots__ = ('debug',)
	
	def __init__(self, debug=False):
		self.debug = debug
			

	def scrape_medium(self) -> Tag:
		"""
		Scrapes medium and returns its body tag.
		
		Returns
		-------
		body : Tag
		body Tag object
		"""
		options = Options()
		options.headless = True
		options.add_experimental_option('excludeSwitches', ['enable-logging'])	
		if exe_path:
			driver = Chrome(executable_path="database/chromedriver.exe", options=options)
		else:
			driver = Chrome(options=options)
		driver.get('https://medium.com/@devblogwows')
		source = driver.page_source.encode('utf-8')
		driver.quit()
		
		if self.debug:
			with open('medium.html', 'w', encoding='utf-8') as f:
				f.write(str(source))
		soup = BeautifulSoup(source, 'html.parser')
		body = soup.body
		return body
		

	def debug_scrape_medium(self) -> Tag:
		"""
		Using saved medium.html, returns its body tag.

		Returns
		-------
		body : Tag
			body Tag object
		"""
		try:
			with open('medium.html', 'r', encoding='utf-8') as f:
				return BeautifulSoup(f.read(), 'html.parser')
		except:
			return self.scrape_medium()


	def get_section_tag(self, body: Tag) -> Tag:
		"""
		Returns section Tag object from body.

		Parameters
		----------
		body : Tag
			body Tag object
		
		Returns
		-------
		section : Tag
			section Tag object
		"""
		root = body.find('div', {'id':'root'})
		section = root.findNext('section')
		if self.debug:
			with open('section.html', 'w', encoding='utf-8') as f:
				f.write(str(section))
		return section


	def get_raw_article_div(self, section: Tag) -> Tag:
		"""
		Returns articles Tag object from section Tag object.

		Parameters
		----------
		section : Tag
			section Tag object
		
		Returns
		-------
		articles : Tag
			article Tag object
		"""
		temp = section.findNext('div')
		articles = temp.next_sibling.div
		if self.debug:
			with open('articles.html', 'w', encoding='utf-8') as f:
				f.write(str(articles))
		return articles


	def get_article_lists(self, articles: Tag) -> list:
		"""
		Returns list of articles processed from articles Tag object.

		Parameters
		----------
		articles : Tag
			articles Tag object
		
		Returns
		-------
		article_list
			list of articles
		"""
		article_list = []
		counter = 0
		for article in articles:
			counter += 1
			if counter <= 1:
				continue
			if article == '\n' or article == '\n\n':
				continue
			if self.debug:
				with open('article.html', 'w', encoding='utf-8') as f:
					f.write(str(article))
			div = article.div.div.next_sibling
			if self.debug:
				with open('div_article.html', 'w', encoding='utf-8') as f:
					f.write(str(div))
			url = str('https://medium.com' + div.find('a')['href']).split('?source=')[0]
			try:
				img = str(div.find('img')['src'])
			except:
				img = 'None'
			title = ''
			description = ''
			for string in div.strings:
				if string == '\n':
					continue
				if title == '':
					title += string
				else:
					description += string
			if description == '':
				description = title
			tp = ('medium', title, description, url, img)
			article_list.append(tp)
		if self.debug:
			with open('medium.json', 'w', encoding='utf-8') as f:
				f.write(json.dumps(article_list, indent=4, ensure_ascii=False))
		return article_list


def get_medium_articles(debug=False):
	medium = Medium(debug=debug)
	body = medium.scrape_medium()
	section = medium.get_section_tag(body)
	articles = medium.get_raw_article_div(section)
	temp = medium.get_article_lists(articles)
	# sometimes scraping does not work
	if not temp:
		raise ScrapingException('Unable to scrape articles.')

	return temp
	

# if __name__ == '__main__':
# 	m = Scrape_medium(debug=True)
# 	with open('temp.json', 'w', encoding='utf-8') as f:
# 		f.write(json.dumps(m.scrape_medium(True), indent=4, ensure_ascii=False))
