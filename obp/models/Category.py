__author__ = 'One Bad Panda'
from obp import db
from slugify import slugify


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    slug = db.Column(db.String())
    posts = db.relationship('Post', backref='category', lazy='dynamic')

    def __init__(self, name, slug=None):
        self.name = name
        slug=slugify(name,max_length=40,word_boundary=True)
        if Category.query.filter_by(slug=slug).all():
            length = len(Category.query.filter(Category.slug.like("%"+slug+"%")).all())
            self.slug = "%s-%i"%(slug, length+1)
        else:
            self.slug = slug

    def __repr__(self):
        return '<Category %r>' % self.name