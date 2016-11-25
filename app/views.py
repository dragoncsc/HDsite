from app import app, db
from flask import render_template, request, url_for, redirect
import requests
from models import Task
import sqlite3
from parse_task import process_tasks



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
def travels():
  tasks = Task.query.all()
  for u in tasks:
    print(u.id, u.taskname)
  if request.method == "POST":
    print request.form['taskname'], request.form['daterange'], request.form['Type']
    cur = Task(taskname=request.form['taskname'], date=request.form['daterange'], type=request.form['Type'])
    db.session.add(cur)
    db.session.commit()
  process = process_tasks()
  tasks = Task.query.all()
  all_tasks = process.parse_tasks( tasks )
  return render_template('priority.html',
      title='Prioritizer', tasks=all_tasks)



@app.route("/search.html", methods=["GET", "POST"])
@app.route("/search", methods=["GET", "POST"])
def search():
  if request.method == "POST":
    url = "https://api.github.com/search/repositories?q=" + request.form["user_search"]
    response_dict = requests.get(url).json()
    return render_template("results.html", api_data=response_dict)
  else:
    return render_template("search.html")


@app.route('/lonely.html')
@app.route('/lonely')
def lonely():
  return render_template('lonely.html',
                         title='Lonely')


@app.route('/user')
def user():
  user = {'nickname': 'Miguel'}
  posts = [  # fake array of posts
        {
            'author': {'nickname': 'John'},
            'body': 'Beautiful day in Portland!'
        },
        {
            'author': {'nickname': 'Susan'},
            'body': 'The Avengers movie was so cool!'
        }
  ]
  return render_template('user.html',
                         title='User',
                         user=user,
                         posts=posts)


@app.route('/login.html', methods=["GET", "POST"])
@app.route('/login', methods=["GET", "POST"])
# route for handling the login page logic
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != 'admin' or request.form['password'] != 'admin':
            error = 'Invalid Credentials. Please try again.'
        else:
            return redirect(url_for('travels'))
    return render_template('login.html', error=error)




@app.errorhandler(404)
def page_not_found(error):
  return render_template("404.html",
                        title="Not Found")

'''
@app.errorhandler(InvalidUsage)
def handle_invalid_usage(error):
  response = jsonify(error.to_dict())
  response.status_code = error.status_code
  return response
'''






