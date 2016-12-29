

import feedparser

hit_list = [ 'http://rss.nytimes.com/services/xml/rss/nyt/MostViewed.xml', 'http://rss.nytimes.com/services/xml/rss/nyt/Technology.xml' ]

feed = feedparser.parse( hit_list[0] )

print feed
