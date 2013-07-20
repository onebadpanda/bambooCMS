__author__ = 'One Bad Panda'
from flask.ext.wtf import Form, RecaptchaField
from wtforms import TextField, BooleanField, TextAreaField
from wtforms.validators import Required, EqualTo, Email, DataRequired
from wtforms.fields import PasswordField


class RegisterForm(Form):
    first_name = TextField('First name', [Required()])
    last_name = TextField('Last name', [Required()])
    username = TextField('Username', [Required()])
    email = TextField('Email address', [Required(), Email()])
    password = PasswordField('Password', [Required()])
    confirm = PasswordField('Repeat Password',
                            [Required(), EqualTo('password', message='Passwords must match')])
    accept_tos = BooleanField('I accept the TOS', [Required()])
    recaptcha = RecaptchaField()


class LoginForm(Form):
    username = TextField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember me', default=False)

class CommentForm(Form):
    body = TextAreaField('Comments:', validators=[DataRequired()])
