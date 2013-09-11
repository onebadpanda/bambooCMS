__author__ = 'One Bad Panda'
from flask.ext.wtf import ListWidget, CheckboxInput,  Form, TextField, TextAreaField, PasswordField, SelectField, SelectMultipleField
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


class MultiCheckboxField(SelectMultipleField):
    widget = ListWidget(prefix_label=False)
    option_widget = CheckboxInput()

def categories():
    return Category.query.with_entities(Category.id, Category.name).order_by(Category.name).all()


def users():
    return User.query.with_entities(User.id, User.username).order_by(User.username).all()


def tags():
    return Tag.query.with_entities(Tag.id, Tag.name).order_by(Tag.name).all()


def posts():
    return Post.query.with_entities(Post.id, Post.title).order_by(Post.pub_date).all()

class UserForm(Form):
    first_name = TextField('first name', [Required()])
    last_name = TextField('last name', [Required()])
    username = TextField('user name', [Required()])
    email = TextField('email address', [Required(), Email()])
    role = SelectField('role', choices=USER_ROLE.items(), coerce=int)
    status = SelectField('status', choices=USER_STATUS.items(), coerce=int)


class UserNew(UserForm):
    password = PasswordField('password', [Required()])


class UserEdit(UserForm):
    pass

class PostForm(Form):
    title = TextField('title', [Required()])
    body = TextAreaField('body', [Required()])
    category_id = SelectField('category', choices=categories(), coerce=int)

class PostNew(PostForm):
    tags = MultiCheckboxField(choices=tags(),coerce=int)
    status = SelectField('status', choices=POST_STATUS.items(), coerce=int)


class PostEdit(PostForm):
    user_id = SelectField('author', choices=users(), coerce=int)
    tags = MultiCheckboxField(choices=tags(),coerce=int)
    status = SelectField('status', choices=POST_STATUS.items(), coerce=int)


class CategoryForm(Form):
    name = TextField('name',[Required()])


class TagForm(Form):
    name = TextField('name',[Required()])