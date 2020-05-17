# Newscatcher

Newscatcher allows you to easily search our database of news rss feeds and display their contents based on your criteria, connecting you instantly to articles and information from 1000s of different news outlets.

**website** [Newscatcher](https://newscatcherapi.com/)

## Installation

```bash
pip install newscatcher
```

## Usage

urls and describe_url
```python
from newscatcher import urls, describe_url


politic_urls = urls(topic = 'politics') # set topic, language, and/or country
american_urls = urls(country = 'US')
american_politics_urls = urls(country = 'US', topic = 'politics')

websites = urls(topic = 'finance', language = 'en') 
#bloomberg.com, yahoofinance.com ...

ret = describe_url(websites[0])#bloomberg.com
ret = {'url' : 'bloomberg.com', 'language' : 'en', 'country' : 'us' , 'topics' : topics} #topics = topics offered by this url, useful when creating the Newscatcher object
```

Analyzing articles
```python
from newscatcher import Newscatcher

nc = Newscatcher(website = 'nytimes.com')
results = nc.search()
articles = results['articles']

summaries = articles['summary']
titles = articles['title']


#usage with optional topic field

nc = Newscatcher(website = 'nytimes.com', topic = 'politics') #topics available for a website, may be found with the describe_url function

results = nc.search()
articles = results['articles']
