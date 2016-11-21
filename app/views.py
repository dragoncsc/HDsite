from app import app
from flask import render_template

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


@app.route('/travels.html')
@app.route('/travels')
def travels():
  return render_template('travels.html',
                         title='Travels')


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

@app.errorhandler(404)
def page_not_found(error):
  return render_template("404.html",
                        title="Not Found")









