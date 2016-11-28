from app import app, db
from flask import render_template, request, url_for, redirect
import requests
from models import Article, Impressions
import sqlite3
from parse_task import process_tasks

process = process_tasks()

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
      title='Prioritizer', tasks=process.get_all_articles())


@app.route('/history.html', methods=["GET", "POST"])
@app.route('/history', methods=["GET", "POST"])
def history():
  return render_template('history.html',
      title='Prioritizer', tasks=process.get_all_impressions())



@app.route('/updatequeue', methods=['POST'])
def updatequeue():
  print request.form
  cur = Article.query.filter_by( id=request.form['_article'] ).first()
  if 'save' in request.form:
    thought = 'None'
    artcat = 'None'
    if 'thoughts' in request.form:
      thought = request.form['thoughts']
    if 'ArtCat' in request.form:
      artcat = request.form['ArtCat']
    impression = Impressions( thoughts=thought, category=artcat, title=cur.title, source=cur.source )
    db.session.add(impression)
    db.session.commit()
  if '_article' in request.form:
    db.session.delete(cur)
    db.session.commit()
  return render_template('priority.html',
      title='Prioritizer', tasks=process.get_all_articles())

@app.errorhandler(404)
def page_not_found(error):
  return render_template("404.html",
                        title="Not Found")






