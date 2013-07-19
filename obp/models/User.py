__author__ = 'One Bad Panda'
from flask.ext.login import UserMixin
from obp import db
from obp import bcrypt
from obp.constants import user as USER


class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(80))
    last_name = db.Column(db.String(80))
    username = db.Column(db.String(80), unique=True)
    email = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(160))
    role = db.Column(db.SmallInteger, default=USER.USER)
    status = db.Column(db.SmallInteger, default=USER.NEW)
    activation_hash = db.Column(db.String)
    posts = db.relationship('Post', backref='author', lazy='dynamic')
    comments = db.relationship('Comment', backref='author', lazy='dynamic')

    def __init__(self, first_name=None, last_name=None, username=None, email=None, password=None,
                 role=USER.USER, status=USER.NEW, activation_hash=None):
        self.first_name = first_name
        self.last_name = last_name
        self.username = username
        self.email = email
        self.password = bcrypt.generate_password_hash(password, 10)
        self.role = role
        self.status = status
        self.activation_hash = activation_hash

    def __repr__(self):
        return '<User %r>' % self.username

    def get_status(self):
        return USER.STATUS[self.status]

    def get_role(self):
        return USER.ROLE[self.role]

    def check_password(self, provided_pass):
        return bcrypt.check_password_hash(self.password, provided_pass)
