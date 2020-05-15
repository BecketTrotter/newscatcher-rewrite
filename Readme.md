# Newscatcher

Newscatcher allows you to easily search our database of news rss feeds and display their contents based on your criteria, connecting you instantly to articles and information from 1000s of different news outlets.

**website** [Newscatcher](https://newscatcherapi.com/)

## Installation

```bash
pip install newscatcher
```

## Usage

Searching for urls
```python
from newscatcher import Newscatcher, urls, describe_url

websites = urls(topic = 'finance', language = 'en') # set topic, language, country
#bloomberg.com, yahoofinance.com ...

describe_url(websites[0])#bloomberg.com
ret = {'url' : 'bloomberg.com', 'language' : 'en', 'country' : 'us' , 'topics' : topics}
```

Analyzing articles

```python
from newscatcher import Newscatcher

nc = Newscatcher(website = 'nytimes.com')
results = nc.search() 
articles = results['articles']

summaries = [article['summary'] for article in articles]
titles = [article['title'] for article in articles]
