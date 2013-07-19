__author__ = 'One Bad Panda'
from flask.ext.wtf import Form, TextField, TextAreaField, PasswordField, SelectField
from wtforms.validators import Required, Email
from wtforms.widgets import Select
from obp.constants.user import ROLE as USER_ROLE
from obp.constants.user import STATUS as USER_STATUS
from obp.constants.post import STATUS as POST_STATUS
from obp.models.User import User
from obp.models.Post import Post
from obp.models.Category import Category
from obp.models.Tag import Tag


#create select widget for USER ROLE
class ChoicesSelect(Select):
    def __init__(self, multiple=False, choices=()):
        self.choices = choices
        super(ChoicesSelect, self).__init__(multiple)

    def __call__(self, field, **kwargs):
        field.iter_choices = lambda: ((val, label, val == field.data)
                                      for val, label in self.choices)
        return super(ChoicesSelect, self).__call__(field, **kwargs)


def categories():
    return Category.query.with_entities(Category.id, Category.name).order_by(Category.name).all()


def users():
    return User.query.with_entities(User.id, User.username).order_by(User.username).all()


def tags():
    return Tag.query.with_entities(Tag.id, Tag.name).order_by(Tag.name).all()


def posts():
    return Post.query.with_entities(Post.id, Post.title).order_by(Post.pub_date).all()


class UserNew(Form):
    first_name = TextField('first name', [Required()])
    last_name = TextField('last name', [Required()])
    username = TextField('user name', [Required()])
    email = TextField('email address', [Required(), Email()])
    password = PasswordField('password', [Required()])
    role = SelectField('role', choices=USER_ROLE.items(), coerce=int)
    status = SelectField('status', choices=USER_STATUS.items(), coerce=int)


class UserEdit(Form):
    first_name = TextField('first name', [Required()])
    last_name = TextField('last name', [Required()])
    username = TextField('user name', [Required()])
    email = TextField('email address', [Required(), Email()])
    role = SelectField('role', choices=USER_ROLE.items(), coerce=int)
    status = SelectField('status', choices=USER_STATUS.items(), coerce=int)


class PostNew(Form):
    title = TextField('title', [Required()])
    body = TextAreaField('body', [Required()])
    category_id = SelectField('category', choices=categories(), coerce=int)
    #tags = SelectField('tags', choices=tags().items(),coerce=int)
    status = SelectField('status', choices=POST_STATUS.items(), coerce=int)


class PostEdit(Form):
    title = TextField('title', [Required()])
    body = TextAreaField('body', [Required()])
    category_id = SelectField('category', choices=categories(), coerce=int)
    user_id = SelectField('author', choices=users(), coerce=int)
    #tags = SelectField('tags', choices=tags().items(),coerce=int)
    status = SelectField('status', choices=POST_STATUS.items(), coerce=int)


class CategoryNew(Form):
    name = TextField('name',[Required()])


class TagNew(Form):
    name = TextField('name',[Required()])