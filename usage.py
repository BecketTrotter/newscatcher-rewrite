from feedparser import parse

rss_endpoint = 'http://www.lemonde.fr/rss/tag/international.xml'
feed = parse(rss_endpoint)
print(feed['entries'])