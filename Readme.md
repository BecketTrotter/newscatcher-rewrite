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
american_english_politics_urls = urls(country = 'US', topic = 'politics', language = 'en') 
#note some websites do not explicitly declare their language 
#as a result they will be excluded from queries based on language

websites = urls(topic = 'finance', language = 'en') 
#bloomberg.com, yahoofinance.com ...

ret = describe_url(websites[0])#bloomberg.com
ret = {'url' : 'bloomberg.com', 'language' : 'en', 'country' : 'us' , 'topics' : topics} #topics = topics offered by this url, useful when creating the Newscatcher object
```

articles / titles
```python
from newscatcher import Newscatcher

nc = Newscatcher(website = 'nytimes.com')
results = nc.get_news()

#results.keys() = 'url', 'language', 'country', 'articles'


articles = results['articles']

first_article_summary = articles[0]['summary']
first_article_title = articles[0]['title']

#usage with optional topic field

nc = Newscatcher(website = 'nytimes.com', topic = 'politics') #topics available for a website, may be found with the describe_url function

results = nc.get_news()
articles = results['articles']
```

## Country Codes
'US', 'GB', 'DE', 'FR', 'IN', 'RU', 'ES', 'BR', 'IT', 'CA', 'AU', 'NL', 'PL', 'NZ', 'PT', 'RO', 'UA', 'JP', 'AR', 'IR', 'IE', 'PH', 'IS', 'ZA', 'AT', 'CL', 'HR', 'BG', 'HU', 'KR', 'SZ', 'AE', 'EG', 'VE', 'CO', 'SE', 'CZ', 'ZH', 'MT', 'AZ', 'GR', 'BE', 'LU', 'IL', 'LT', 'NI', 'MY', 'TR', 'BM', 'NO', 'ME', 'SA', 'RS', 'BA'

## Topics
'tech', 'news', 'business', 'science', 'finance', 'food', 'politics', 'economics', 'travel', 'entertainment', 'music', 'sport', 'world'

## Languages
'EL', 'IT', 'ZH', 'EN', 'RU', 'CS', 'RO', 'FR', 'JA', 'DE', 'PT', 'ES', 'AR', 'HE', 'UK', 'PL', 'NL', 'TR', 'VI', 'KO', 'TH', 'ID', 'HR', 'DA', 'BG', 'NO', 'SK', 'FA', 'ET', 'SV', 'BN', 'GU', 'MK', 'PA', 'HU', 'SL', 'FI', 'LT', 'MR', 'NONE', 'HI'