__author__ = 'One Bad Panda'
from obp import db


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    posts = db.relationship('Post', backref='category', lazy='dynamic')

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return '<Category %r>' % self.name