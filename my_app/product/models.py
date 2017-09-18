from my_app import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_wtf import FlaskForm
from wtforms import TextField, PasswordField
from wtforms.validators import InputRequired, EqualTo
from flask_wtf.csrf import CSRFProtect

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255))
    pwdhash = db.Column(db.String(100))

    def __init__(self, username, password):
        self.username = username
        self.pwdhash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.pwdhash, password)

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return unicode(self.id)

class LoginForm(FlaskForm):
    username = TextField('Username', [InputRequired()])
    password = PasswordField('Password', [InputRequired()])

class RegistrationForm(FlaskForm):
    username = TextField('Username', [InputRequired()])
    password = PasswordField('Password', [InputRequired(), EqualTo('confirm', message='Passwordsmust match')])
    confirm = PasswordField('Confirm Password', [InputRequired()])

class envLabels(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    envLabel = db.Column(db.String(255))
    envName = db.Column(db.String(255))
    orderProp = db.Column(db.String(255))
    provFile = db.Column(db.String(255))

    def __init__(self, envLabel, envName, orderProp, provFile):
        self.envLabel = envLabel
        self.envName = envName
        self.orderProp = orderProp
        self.provFile = provFile

    def __repr__(self):
        return '<Environment %d>' % self.id

class faatLabels(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    faatLabel = db.Column(db.String(255))

    def __init__(self, faatLabel):
        self.faatLabel = faatLabel

    def __repr__(self):
        return '<FAAT LAbel : %d>' % self.faatLabel

class centralenvs(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    envLabel = db.Column(db.String(255))
    envName = db.Column(db.String(255))
    orderProp = db.Column(db.String(255))
    provFile = db.Column(db.String(255))

    def __init__(self, envLabel, envName, orderProp, provFile):
        self.envLabel = envLabel
        self.envName = envName
        self.orderProp = orderProp
        self.provFile = provFile

    def __repr__(self):
        return '<Environment %d>' % self.id