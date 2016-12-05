from app import db

class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    link = db.Column(db.String(250), index=True)
    title = db.Column(db.String(140), index=True)
    source = db.Column(db.String(50), index=True)
    reader = db.Column( db.String, db.ForeignKey('user.username') )

    def __repr__(self):
        return '<Task %r>' % (self.title)


class Impressions(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    thoughts = db.Column(db.String(500), index=True)
    title = db.Column(db.String(140), index=True)
    category = db.Column(db.String(50), index=True)
    source = db.Column(db.String(50), index=True)
    writer = db.Column( db.String, db.ForeignKey('user.username') )

    def __repr__(self):
        return '<Task %r>' % (self.title)


class User(db.Model):

    __tablename__ = 'user'

    username = db.Column(db.String, primary_key=True)
    password = db.Column(db.String)
    authenticated = db.Column(db.Boolean, default=False)
    articles = db.relationship( 'Article', backref='_reader', 
    	lazy='dynamic' )
    impression = db.relationship( 'Impressions', backref='_writer', 
    	lazy='dynamic' )

    def is_active(self):
        """True, as all users are active."""
        return True

    def get_id(self):
        """Return the email address to satisfy Flask-Login's requirements."""
        return self.username

    def is_authenticated(self):
        """Return True if the user is authenticated."""
        return self.authenticated

    def is_anonymous(self):
        """False, as anonymous users aren't supported."""
        return False
















