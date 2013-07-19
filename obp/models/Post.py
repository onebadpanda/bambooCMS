__author__ = 'One Bad Panda'
from datetime import datetime
from obp import db
from obp.constants import post as POST


class Post(db.Model):
    __tablename__ = 'post'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String())
    body = db.Column(db.Text())
    create_date = db.Column(db.DateTime)
    pub_date = db.Column(db.DateTime)
    status = db.Column(db.SmallInteger)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))

    def __init__(self, user_id, title, body, category_id, create_date=None, pub_date=None, status=None):
        self.user_id = user_id
        self.title = title
        self.body = body
        self.category_id = category_id
        if create_date is None:
            create_date = datetime.utcnow()
        self.create_date = create_date
        self.pub_date = pub_date
        if status is None:
            status = POST.DRAFT
        self.status = status

    def __repr__(self):
        return '<Post %r>' % self.title

    def get_status(self):
        return POST.STATUS[self.status]