from app import db

class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    link = db.Column(db.String(250), index=True)
    title = db.Column(db.String(140), index=True)
    source = db.Column(db.String(50), index=True)

    def __repr__(self):
        return '<Task %r>' % (self.title)


class Impressions(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    thoughts = db.Column(db.String(500), index=True)
    title = db.Column(db.String(140), index=True)
    category = db.Column(db.String(50), index=True)

    def __repr__(self):
        return '<Task %r>' % (self.title)



