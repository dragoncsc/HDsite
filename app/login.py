from flask.ext.wtf import FlaskForm
from wtforms import  TextField, PasswordField, validators, Form
from models import User
import hashlib


class LoginForm(FlaskForm):
    username = TextField('Username', [validators.Required()])
    sha224 = hashlib.sha224()
    password = PasswordField('Password', [validators.Required()])

    def __init__(self, *args, **kwargs):
        FlaskForm.__init__(self, *args, **kwargs)
        self.user = None

    def validate(self):
        rv = Form.validate(self)
        if not rv:
            return False
        user = User.query.filter_by(
            username=self.username.data).first()
        if user is None:
            self.username.errors.append('Unknown username')
            return False
        hashed = hashlib.sha224()
        hashed.update(self.password.data)
        print "In validation: ", hashed.hexdigest()
        if user.password != hashed.hexdigest():
            self.password.errors.append('Invalid password')
            return False
        self.user = user
        return True



def login_user( user ):
  User.query.get( username=user )