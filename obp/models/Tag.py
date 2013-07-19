__author__ = 'One Bad Panda'
from obp import db


tags = db.Table('tags',
                db.Column('tag_id', db.Integer, db.ForeignKey('tag.id')),
                db.Column('post_id', db.Integer, db.ForeignKey('post.id')),
                )


class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return '<Tag %r>' % self.name