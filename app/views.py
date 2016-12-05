from app import app, db
from flask import render_template, request, url_for, redirect, flash, session
import requests
from models import Article, Impressions, User
import sqlite3
from parse_task import process_articles
from urlparse import urlparse, urljoin
from flask_login import LoginManager, login_user, current_user
from login import LoginForm
from flask.ext.security import login_required
import hashlib

backend_article_handler = process_articles()
catagories = ['Left', 'Right', 'Centrist', 'Economy', 'Sports', 'News']
login_manager = LoginManager()
login_manager.init_app(app)

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
@login_required
def priority():
  if request.method == "POST":
    cur = Article(link=request.form['link'], title=request.form['Title'], 
      source=request.form['Type'], reader=current_user.username)
    db.session.add(cur)
    db.session.commit()
  return render_template('priority.html',
      title='Prioritizer', tasks=backend_article_handler.get_all_articles(current_user.username), 
      user=current_user)


@app.route('/history.html', methods=["GET", "POST"])
@app.route('/history', methods=["GET", "POST"])
@login_required
def history():
  return render_template('history.html',
      title='Prioritizer', tasks=backend_article_handler.get_all_impressions(current_user.username))


@app.route('/updatequeue', methods=['POST'])
@login_required
def updatequeue():
  data = request.get_json(silent=True)
  cur = Article.query.filter_by( id=data['articleId'] ).first()
  cat = None
  for i in xrange(len(data['checkbox'])):
    if data['checkbox'][i]:
      cat=catagories[i]
      break
  impression = Impressions( thoughts=data['impression'], category=i, title=cur.title, 
    source=cur.source, writer=current_user.username )
  db.session.add(impression)
  db.session.commit()
  backend_article_handler.destroy_article( cur )
  return render_template('priority.html',
      title='Prioritizer', tasks=backend_article_handler.get_all_articles())


@app.route('/destroy_article', methods=['DELETE'])
@login_required
def get_id_for_deletion(  ):
  data = request.get_json(silent=True)
  article = Article.query.get(data["articleId"])
  if article != None:
    return backend_article_handler.destroy_article( article )
  return url_for('priority')


@app.route('/login.html', methods=['GET', 'POST'])
@app.route('/login', methods=['GET', 'POST'])
def login():
    # for new users
    for user in User.query.all():
      print user.username
      print user.password
    if 'newusername' in request.form:
      return addNewUser(request)
    
    # for already existing users
    form = LoginForm()
    if not form.validate():
      render_template('login.html', form=form)
    if form.validate_on_submit():
        login_user( form.user )
        flash('Logged in successfully.')
        next = request.args.get('next')
        if not is_safe_url(next):
            return flask.abort(400)
        return redirect(next or url_for('priority'))
    else:
      print form.errors
    return render_template('login.html', form=form)

@login_manager.user_loader
def user_loader(username):
    """Given *user_id*, return the associated User object.

    :param unicode user_id: user_id (email) user to retrieve
    """
    return User.query.get(username)

@app.errorhandler(404)
def page_not_found(error):
  return render_template("404.html",
                        title="Not Found")


def addNewUser( request ):
  if User.query.get( request.form['newusername'] ):
    flash("Username is already taken")
    return render_template('login.html')
  else:
    if request.form['newpassword1'] != request.form['newpassword2']:
      flash('Passwords do not match')
      return render_template('login.html')
    sha224 = hashlib.sha224()
    sha224.update(request.form['newpassword2'])
    print sha224.hexdigest()
    cur = User( username=request.form['newusername'], password=sha224.hexdigest(), authenticated=True )
    db.session.add(cur)
    db.session.commit()
    flash("Please Log in with your new account")
    return render_template('login.html')

def is_safe_url(target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and \
           ref_url.netloc == test_url.netloc



