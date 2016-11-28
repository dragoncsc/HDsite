
from models import Article, Impressions


class process_tasks():

	def __init__(self):
		self.sources_img= { 'ECONOMIST':'../static/images/economist.jpg', 'BBC':'../static/images/bbc.jpg', 
			"WASHINGTON POST": '../static/images/wp.jpg', "NYTIMES": '../static/images/nyt.jpg',
			"TIMES OF LONDON":'../static/images/thetimes.jpg'}
		self.library = '../static/images/library.jpg'
	
	def parse_tasks(self, from_db ):
		all_tasks = []
	
		for u in from_db:
			if u.source.upper() in self.sources_img:
				all_tasks.append( ( u.title.upper(), u.link, u.source, self.sources_img[u.source.upper()], u.id) )
			else:
				all_tasks.append( ( u.title.upper(), u.link, u.source, self.library, u.id) )
		return all_tasks

	def parse_impressions(self, from_db ):
		all_tasks = []
		
		if len(from_db) == 0:
			return None

		for u in from_db:
			if u.source.upper() in self.sources_img:
				all_tasks.append( ( u.title.upper(), u.thoughts, u.category, u.source, self.sources_img[u.source.upper()], u.id) )
			else:
				all_tasks.append( ( u.title.upper(), u.thoughts, u.category, u.source, self.library, u.id) )
		return all_tasks

	def get_all_impressions( self ):
		tasks = Impressions.query.all()
		all_tasks = self.parse_impressions( tasks )
		return all_tasks		

	def get_all_articles( self ):
		tasks = Article.query.all()
		all_tasks = self.parse_tasks( tasks )
		return all_tasks



