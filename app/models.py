from app import db

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    taskname = db.Column(db.String(70), index=True)
    date = db.Column(db.String(140), index=True)
    type = db.Column(db.String(50), index=True)

    def __repr__(self):
        return '<Task %r>' % (self.taskname)






