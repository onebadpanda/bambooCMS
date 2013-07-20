__author__ = 'One Bad Panda'
from datetime import datetime
from obp import db


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    create_date = db.Column(db.DateTime)
    body = db.Column(db.Text)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'))

    def __init__(self, user_id, post_id, create_date=None, body=None):
        self.user_id = user_id
        self.post_id = post_id
        if create_date is None:
            create_date = datetime.utcnow()
        self.create_date = create_date
        self.body = body
        #TODO figure out relationships needed for this class
        #TODO one->many relationship post->comment
        #TODO one->many relationship user(as comment author)->comment

    def __repr__(self):
        pass