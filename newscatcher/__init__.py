#Retrieve and analyze
#24/7 streams of news data
import sys
import sqlite3
import requests
import feedparser
import pkg_resources
from tldextract import extract


DB_FILE = pkg_resources.resource_filename('newscatcher', 'data/package_rss.db')
#DB_FILE = 'data/package_rss.db'

class Query:
	#Query class used to build subsequent sql queries
	def __init__(self):
		self.params = {'website': None, 'topic': None}

	def build_conditional(self, field, sql_field):
		#single conditional build
		field = field.lower()
		sql_field = sql_field.lower()

		if self.params[field] != None:
			conditional = "{} = '{}'".format(sql_field, self.params[field])
			return conditional
		return


	def build_where(self):
		#returning the conditional from paramters
		#the post "WHERE"
		conditionals = []

		conv = {'topic' : 'topic_unified', 'website' : 'clean_url'}

		for field in conv.keys():
			cond = self.build_conditional(field, conv[field])
			if cond != None:
				conditionals.append(cond)

		if conditionals == []:
			return

		conditionals[0] = 'WHERE ' + conditionals[0]
		conditionals = ''' AND '.join([x for x in conditionals if x != None])
		+ ' ORDER BY IFNULL(Globalrank,999999);'''


		return conditionals


	def build_sql(self):
		#build sql on user qeury
		db = sqlite3.connect(DB_FILE, isolation_level=None)
		sql = 'SELECT rss_url from rss_main ' + self.build_where()

		db.close()
		return sql


def unique(field):
	#return unique values from given field
	field = field.lower()
	alt = {'country' : 'clean_country', 'url' : 'clean_url', 'topic' : 'topic_unified',
		   'language' : 'language', 'website' : 'clean_url'}
	vals = [alt[x] for x in alt.keys()]

	if field not in alt.keys() and field not in vals:
		sys.exit('{} not in {}'.format(field, vals))

	if field in alt.keys():
		field = alt[field]

	sql = 'SELECT DISTINCT {} FROM rss_main;'.format(field)
	db = sqlite3.connect(DB_FILE, isolation_level=None)
	try:
		ret = [x[0] for x in db.execute(sql).fetchall()]
	except:
		db.close()
	db.close()
	return ret


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


class Newscatcher:
	#search engine
	def __init__(self, website, topic=None):
		#init with given params
		website = website.lower()
		self.q = Query()
		website = clean_url(website)
		self.q.params = {'website' : website, 'topic' : topic}

	def search(self, n=None):
		#return results based on current stream
		sql = self.q.build_sql()
		db = sqlite3.connect(DB_FILE, isolation_level=None)

		try:
			rss_endpoint = db.execute(sql).fetchone()[0]
			feed = feedparser.parse(rss_endpoint)
		except:
			db.close()
			sys.exit('\nWebsite is not supported\n')


		if feed['entries'] == []:
			db.close()
			sys.exit('\nno results found check internet connection or query paramters\n')

		if n == None or len(feed['entries']) <= n:
			articles = feed['entries']#['summary']#[0].keys()
		else:
			articles = feed['entries'][:n]

		sql = '''SELECT topic_unified, language, clean_country 
				 FROM rss_main WHERE clean_url = '{}' and main = 1;'''

		sql = sql.format(self.q.params['website'])

		topic, language, country = db.execute(sql).fetchone()

		meta = {'url' : self.q.params['website'], 'topic' : topic,
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
