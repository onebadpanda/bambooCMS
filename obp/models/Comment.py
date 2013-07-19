__author__ = 'One Bad Panda'
from datetime import datetime
from obp import db


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    create_date = db.Column(db.DateTime)
    body = db.Column(db.Text)

    def __init__(self, create_date=None, body=None):
        if create_date is None:
            self.body = datetime.utcnow()
        self.body = body
        #TODO figure out relationships needed for this class
        #TODO one->many relationship post->comment
        #TODO one->many relationship user(as comment author)->comment

    def __repr__(self):
        pass