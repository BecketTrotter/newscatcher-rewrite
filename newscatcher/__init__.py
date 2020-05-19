#Retrieve and analyze
#24/7 streams of news data
import sys
import sqlite3
import requests
import feedparser
import pkg_resources
from tldextract import extract


DB_FILE = pkg_resources.resource_filename('newscatcher', 'data/package_rss.db')

def clean_url(dirty_url):
	#website.com
	dirty_url = dirty_url.lower()
	o = extract(dirty_url)
	return o.domain + '.' + o.suffix


def classify_url(url, curr):
	#url -> topic_unified, language, clean_country, clean_url
	url = url.lower()
	url = clean_url(url)

	sql = '''SELECT topic_unified, language, clean_country,
	clean_url from rss_main WHERE clean_url = '{}' AND main = 1'''

	ret = curr.execute(sql.format(url)).fetchone()
	return ret


def alt_feed(url):
	db = sqlite3.connect(DB_FILE, isolation_level=None)
	sql = '''SELECT rss_url from rss_main 
					 WHERE clean_url = '{}';'''
	sql = sql.format(url)
	rss_endpoints = db.execute(sql).fetchall()

	for rss_endpoint in rss_endpoints:
		
		rss_endpoint = db.execute(sql).fetchone()[0]
		feed = feedparser.parse(rss_endpoint)
		print(feed)
		if feed['entries'] != []:
			return feed

	db.close()
	return -1



class Newscatcher:
	#search engine
	def build_sql(self):
		if self.topic is None:
			sql = '''SELECT rss_url from rss_main 
					 WHERE clean_url = '{}';'''
			sql = sql.format(self.url)
			return sql

	def __init__(self, website, topic=None):
		#init with given params
		website = website.lower()
		self.url = clean_url(website)
		self.topic = topic

		

	def search(self, n=None):
		#return results based on current stream
		if self.topic is None:
			sql = '''SELECT rss_url from rss_main 
					 WHERE clean_url = '{}' AND main = 1;'''
			sql = sql.format(self.url)
		else:
			sql = '''SELECT rss_url from rss_main 
					 WHERE clean_url = '{}' AND topic_unified = '{}';'''
			sql = sql.format(self.url, self.topic)

		

		db = sqlite3.connect(DB_FILE, isolation_level=None)

		try:
			rss_endpoint = db.execute(sql).fetchone()[0]
			feed = feedparser.parse(rss_endpoint)
		except:
			if self.topic is not None:
				sql = '''SELECT rss_url from rss_main 
					 WHERE clean_url = '{}';'''
				sql = sql.format(self.url)
				
				if len(db.execute(sql).fetchall()) > 0:
					db.close()
					sys.exit('Topic is not supported')
				else:
					sys.exit('Website is not supported')
					db.close()


				
				
				


		if feed['entries'] == []:
			feed = alt_feed(self.url)

			if feed == -1:
				db.close()
				sys.exit('\nno results found check internet connection or query paramters\n')

		if n == None or len(feed['entries']) <= n:
			articles = feed['entries']#['summary']#[0].keys()
		else:
			articles = feed['entries'][:n]

		if self.topic is None:
			sql = '''SELECT topic_unified, language, clean_country 
					 FROM rss_main WHERE clean_url = '{}' and main = 1;'''
			sql = sql.format(self.url)
		else:
			sql = '''SELECT topic_unified, language, clean_country 
					 FROM rss_main WHERE clean_url = '{}' and topic_unified = '{}';'''
			sql = sql.format(self.url, self.topic)

	
		topic, language, country = db.execute(sql).fetchone()

		meta = {'url' : self.url, 'topic' : topic,
				'language' : language, 'country' : country}

		db.close()
		return {'url': meta['url'], 'main_topic' : meta['topic'],
		'language' : meta['language'], 'country' : meta['country'], 'articles':articles}

def describe_url(website):
	#return newscatcher fields that correspond to the url
	website = website.lower()
	website = clean_url(website)
	db = sqlite3.connect(DB_FILE, isolation_level=None)

	sql = "SELECT * from rss_main WHERE clean_url = '{}' and main == 1 ".format(website)
	results = db.execute(sql).fetchone()


	if results == None:
		sys.exit('\nWebsite not supported\n')

	sql = "SELECT topic_unified from rss_main WHERE clean_url = '{}' and main = 1".format(website)
	main = db.execute(sql).fetchone()[0]
	if len(main) == 0:
		sys.exit('\nWebsite note supported\n')
	sql = "SELECT DISTINCT topic_unified from rss_main WHERE clean_url = '{}'".format(website)
	topics = db.execute(sql).fetchall()
	topics = [x[0] for x in topics]

	ret = {'url' : results[0], 'language' : results[1], 'country' : results[4] , 'main topic' : main, 'topics' : topics}

	return ret


def urls(topic = None, language = None, country = None):
	#return urls that matches users parameters
	if language != None:
		language = language.lower()

	if country != None:
		country = country.upper()

	if topic != None:
		topic = topic.lower()

	db = sqlite3.connect(DB_FILE, isolation_level=None)
	quick_q = Query()
	inp = {'topic' : topic, 'language' : language, 'country' : country}
	for x in inp.keys():
		quick_q.params[x] = inp[x]

	conditionals = []
	conv = {'topic' : 'topic_unified', 'website' : 'clean_url',
			'country' : 'clean_country', 'language' : 'language'}

	for field in conv.keys():
		try:
			cond = quick_q.build_conditional(field, conv[field])
		except:
			cond = None

		if cond != None:
			conditionals.append(cond)

	sql = ''

	if conditionals == []:
		sql = 'SELECT clean_url from rss_main '
	else:
		conditionals[0] = ' WHERE ' + conditionals[0]
		conditionals = ' AND '.join([x for x in conditionals if x is not None]) 
		conditionals += ' AND main = 1 ORDER BY IFNULL(Globalrank,999999);'
		sql = 'SELECT DISTINCT clean_url from rss_main' + conditionals

	ret = db.execute(sql).fetchall()
	if len(ret) == 0:
		sys.exit('\nNo websites found for given parameters\n')

	db.close()
	return [x[0] for x in ret]