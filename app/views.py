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



@app.route('/discard', methods=['POST'])
def discard():
  print request.form
  cur = Article.query.filter_by( id=request.form['_article'] ).first()
  db.session.delete(cur)
  db.session.commit()

  return url_for('priority')

@app.errorhandler(404)
def page_not_found(error):
  return render_template("404.html",
                        title="Not Found")






