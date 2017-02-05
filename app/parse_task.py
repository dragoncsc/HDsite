
from models import Article, Impressions, User
from app import app, db
from flask import render_template, request, url_for, redirect
from Queue import Queue
from threading import Thread
import time
import feedparser
import zmq

class process_articles():

	def __init__(self):
		
		self.sources_img= { 'ECONOMIST': "/static/images/economist.jpg", 'BBC':"/static/images/bbc.jpg", 
			"WASHINGTON POST": "/static/images/wp.jpg", "NYTIMES": "/static/images/nyt.jpg",
			"TIMES OF LONDON":"/static/images/thetimes.jpg"}

		self.library = "/static/images/library.jpg"

		self.newsQueue = Queue()
		# RSS feeds so far
		self.rss = {  
					'nyt' : 'http://rss.nytimes.com/services/xml/rss/nyt/MostViewed.xml',
					'techcrunch' : 'http://feeds.feedburner.com/TechCrunch/startups', 
					'soccer' : 'https://www.reddit.com/r/soccer/top/.rss'
					}
		context = zmq.Context()
		self.sock = context.socket(zmq.REQ)
		self.sock.connect( "tcp://127.0.0.1:5678" )

	''' processes for parsing articles so Jinja can render them '''
	def parse_tasks(self, from_db ):
		all_tasks = []
	
		for u in from_db:
			if u.source.upper() in self.sources_img:
				all_tasks.append( ( u.title.upper(), u.link, u.source, 
					self.sources_img[u.source.upper()], u.id) )
			else:
				all_tasks.append( ( u.title.upper(), u.link, u.source, 
					self.library, u.id) )
		return all_tasks

	def parse_impressions(self, from_db ):
		all_tasks = []
		if not from_db or len(from_db) == 0:
			return None
		for u in from_db:
			if u.source.upper() in self.sources_img:
				all_tasks.append( ( u.title.upper(), u.thoughts, u.category, 
					u.source, self.sources_img[u.source.upper()], u.id) )
			else:
				all_tasks.append( ( u.title.upper(), u.thoughts, u.category, 
					u.source, self.library, u.id) )
		return all_tasks

	
	# process that runs forever and collects RSS feed data from
	# different sites to append to thread safe queue
	# that the views.py module will consume when feed.html is
	# accessed
	# EACH ARTICLE parse: should target the following
	# - title[0], link[1], author[2](.lower()), summary[3], tags[4]
	def grab_rss_feeds(self):
		# need to implement a process in the future to parse
		# found articles by relevance to users, perhaps with
		# redis
		self.sock.send( "articles plz" )
		return self.sock.recv()




	''' Processes for rendering articles'''
	def get_all_impressions( self, username ):
		tasks = User.query.get( username ).impression.all()
		all_tasks = self.parse_impressions( tasks )
		return all_tasks		

	def get_all_articles( self, username ):
		tasks = User.query.get( username ).articles.all()
		all_tasks = self.parse_tasks( tasks )
		return all_tasks

	def get_cat_articles( self, username, cat ):
		tasks = User.query.get( username ).impression.filter_by( category=cat ).all()
		all_tasks = self.parse_impressions( tasks )
		return all_tasks

	def destroy_article( self, article ):
		db.session.delete( article )
		db.session.commit()
		return url_for('priority')
	


