
'''
Subprocess that is called from the run.py script

should spawn off a thread that constantly queries a set of RSS feeds
and writes them to a shared piece of memory
	- running continuously, daemon

the main portion of the script should start up zeromq server and be
constantly ready to serve the parsed RSS feeds when the server is 
queried
	- get list of articles from Queue, serialize it, send it over zeroMQ
'''

import feedparser
import time
from collections import deque
import zmq
import cPickle
from threading import Thread, Lock

rss =   {  
		'nyt' : 'http://rss.nytimes.com/services/xml/rss/nyt/MostViewed.xml',
		'techcrunch' : 'http://feeds.feedburner.com/TechCrunch/startups', 
		'soccer' : 'https://www.reddit.com/r/soccer/top/.rss'
		}
sources_img= { 'ECONOMIST': "/static/images/economist.jpg", 'BBC':"/static/images/bbc.jpg", 
			"WASHINGTON POST": "/static/images/wp.jpg", "NYTIMES": "/static/images/nyt.jpg",
			"TIMES OF LONDON":"/static/images/thetimes.jpg"}


def zeroMQ_server( shared_queue, _lock ):
	context = zmq.Context()
	sock = context.socket(zmq.REP)
	sock.bind( "tcp://127.0.0.1:5678" )
	print "\n\n\nI'm running!\n\n\n"

	while True:
		# no parsing needed so far for client messages
		message = sock.recv()
		# ensure that queue has data to prevent deadlock
		# before grabbing mutex
		while len(shared_queue) < 0:
			continue
		# peek at the newest element in shared queue
		# make sure its not being altered right now
		with _lock:
			serialized = cPickle.dumps( shared_queue[-1] )
		# send serialized data
		sock.send( serialized )

def run_scraper( min_interval, shared_queue, _lock ):	

	while True:
		# build new set of parsed articles
		cur_sources = []
		# grab nyt articles
		cur_sources.extend( new_york_times_rss() )
		# grab the shared queue to get rid of old articles
		with _lock:
			if len(shared_queue) > 0:
				shared_queue.popleft()
			shared_queue.append( cur_sources )
		time.sleep( 60 * min_interval )

# Parse Nyt most viewed articles
# 0-PICTURE, 1-title, 2-link, 3-author, 4-summary, 5-tags
def new_york_times_rss():
	# grab nyt rss mosted viewed feed
	feed = feedparser.parse(rss['nyt'])
	stories = []
	for item in feed['entries']:
		tags = []
		for tag in item['tags']:
			tags.append( tag['term'] )
		stories.append(( sources_img['NYTIMES'], item['title'], 
			item['link'], item['author'].lower(), item['summary'],
			 tags ))
	return stories

# initialize thread safe resources
shared_queue = deque()
_lock = Lock()

t = Thread( target=run_scraper, args=( 15, shared_queue, _lock ) )
t.daemon = True
t.start()
zeroMQ_server( shared_queue, _lock )









