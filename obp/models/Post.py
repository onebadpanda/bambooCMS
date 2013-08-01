__author__ = 'One Bad Panda'
from datetime import datetime
from obp import db
from obp.constants import post as POST
from obp.models.Tag import post_tags
from slugify import slugify

class Post(db.Model):
    __tablename__ = 'post'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String())
    body = db.Column(db.Text())
    create_date = db.Column(db.DateTime)
    pub_date = db.Column(db.DateTime)
    status = db.Column(db.SmallInteger)
    slug = db.Column(db.String())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    comments = db.relationship('Comment', backref='post', lazy='dynamic')
    tags = db.relationship('Tag', secondary=post_tags, backref=db.backref('posts', lazy='joined'))


    def __init__(self, user_id, title, body, category_id, slug=None, tags=None, create_date=None, pub_date=None, status=None):
        self.user_id = user_id
        self.title = title
        self.body = body
        self.category_id = category_id
        if tags is not None:
            for tag in tags:
                self.tags.append(tag)
        else:
            self.tags = []
        if create_date is None:
            create_date = datetime.utcnow()
        self.create_date = create_date
        self.pub_date = pub_date
        if status is None:
            status = POST.DRAFT
        self.status = status
        slug=slugify(title, max_length=40, word_boundary=True)
        if Post.query.filter_by(slug=slug).all:
            length = len(Post.query.filter(Post.slug.like("%"+slug+"%")).all())
            self.slug = "%s-%i"%(slug, length+1)
        else:
            self.slug = slug


    def __repr__(self):
        return '<Post %r>' % self.title

    def get_status(self):
        return POST.STATUS[self.status]