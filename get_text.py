import sys
from bs4 import BeautifulSoup
import urllib.request
from urllib.parse import quote
import cleaned
def get_text(url, site_name):#info_soup
	text = ''#여기서 받는 url은 해당 기사 url에 들어간 url임
	source_code_from_URL = urllib.request.urlopen(url)
	soup = BeautifulSoup(source_code_from_URL,'lxml',from_encoding = 'utf-8')
	if site_name == '동아일보':
		content_of_article = soup.select('div.article_txt')
		for item in content_of_article:
			text = text + str(item.find_all(text = True))
	elif site_name == '중앙일보':
		content_of_article = soup.select('div.article_body')
		for item in content_of_article:
			text = text + str(item.find_all(text = True))
	elif site_name == '한겨레':
		content_of_article = soup.select('div.article-body')
		for item in content_of_article:
			text = text + str(item.find_all(text = True))
	text = cleaned.clean_text(text)
	return text
