__author__ = 'One Bad Panda'
from obp import db
from slugify import slugify


post_tags = db.Table('tags',
                db.Column('tag_id', db.Integer, db.ForeignKey('tag.id')),
                db.Column('post_id', db.Integer, db.ForeignKey('post.id')),
                )


class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    slug = db.Column(db.String())

    def __init__(self, name, slug=None):
        self.name = name
        slug=slugify(name, max_length=40, word_boundary=True)
        if Tag.query.filter_by(slug=slug).all:
            length = len(Tag.query.filter(Tag.slug.like("%"+slug+"%")).all())
            self.slug = "%s-%i"%(slug, length+1)
        else:
            self.slug = slug

    def __repr__(self):
        return '<Tag %r>' % self.name