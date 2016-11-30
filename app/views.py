from app import app, db
from flask import render_template, request, url_for, redirect
import requests
from models import Article, Impressions
import sqlite3
from parse_task import process_articles

backend_article_handler = process_articles()
catagories = ['Left', 'Right', 'Centrist', 'Economy', 'Sports', 'News']


class InvalidUsage(Exception):
    status_code = 400

    def __init__(self, message, status_code=None, payload=None):
        Exception.__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv['message'] = self.message
        return rv


@app.route('/')
@app.route('/index')
@app.route('/index.html')
def index():
  return render_template('index.html',
                         title='Home')

@app.route('/about.html')
@app.route('/about')
def about():
  return render_template('about.html',
                         title='About')

@app.route('/priority.html', methods=["GET", "POST"])
@app.route('/priority', methods=["GET", "POST"])
def priority():
  tasks = Article.query.all()
  for u in tasks:
    print(u.id, u.title)
  if request.method == "POST":
    cur = Article(link=request.form['link'], title=request.form['Title'], source=request.form['Type'])
    db.session.add(cur)
    db.session.commit()
  return render_template('priority.html',
      title='Prioritizer', tasks=backend_article_handler.get_all_articles())


@app.route('/history.html', methods=["GET", "POST"])
@app.route('/history', methods=["GET", "POST"])
def history():
  return render_template('history.html',
      title='Prioritizer', tasks=backend_article_handler.get_all_impressions())


@app.route('/updatequeue', methods=['POST'])
def updatequeue():
  data = request.get_json(silent=True)
  print data
  cur = Article.query.filter_by( id=data['articleId'] ).first()
  cat = None
  for i in xrange(len(data['checkbox'])):
    if data['checkbox'][i]:
      cat=catagories[i]
      break
  print cat
  impression = Impressions( thoughts=data['impression'], category=i, title=cur.title, source=cur.source )
  db.session.add(impression)
  db.session.commit()
  backend_article_handler.destroy_article( cur )
  return render_template('priority.html',
      title='Prioritizer', tasks=backend_article_handler.get_all_articles())



@app.route('/destroy_article', methods=['DELETE'])
def get_id_for_deletion(  ):
  data = request.get_json(silent=True)
  article = Article.query.get(data["articleId"])
  if article != None:
    return backend_article_handler.destroy_article( article )
  return url_for('priority')


@app.errorhandler(404)
def page_not_found(error):
  return render_template("404.html",
                        title="Not Found")






