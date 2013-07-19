__author__ = 'One Bad Panda'
import base64
import hashlib
import logging
import random
import re
from dateutil import tz
from markdown import markdown
from flask import Markup
from flask import flash, render_template, redirect, request, session, url_for
from flask.ext.login import current_user, login_user, login_required, logout_user
from sqlalchemy import func
from obp import app, db, mail
from obp.constants import post as post_status
from obp.forms.standard import RegisterForm, LoginForm
from obp.helpers import send_mail
from obp.helpers import tweets
from obp.models.User import User
from obp.models.Post import Post
from obp.models.Category import Category



from_zone = tz.gettz('UTC')
to_zone = tz.tzlocal()

myTweets = tweets.get_latest_tweets()
myMentions = tweets.get_latest_mentions()


def get_activation_hash():
    result = base64.b64encode(hashlib.sha256(str(random.getrandbits(256))).digest(),
                              random.choice(['rA', 'aZ', 'gQ', 'hH', 'hG', 'aR', 'DD'])).rstrip('==')
    return result


@app.template_filter('markdown')
def markdown_filter(data):
    return Markup(markdown(data))

@app.template_filter()
def twitterize(value):
    """Turn twitter names and hashtags into clickable links."""

    name_regex = r'(@(\w+))'
    name_html = r' <a href="https://twitter.com/\2">\1</a>'
    hash_regex = r'(#(\w+))'
    hash_html = r' <a href="https://twitter.com/#search?q=\2">\1</a>'

    try:
        value = re.sub(name_regex, name_html, value)
        value = re.sub(hash_regex, hash_html, value)
        return Markup(value)

    except Exception, ex:
        logging.error('twitterize: %s' % ex)


@app.route('/')
def index():
    active = 'blog'
    posts = Post.query.filter_by(status=post_status.PUBLISHED).order_by(Post.pub_date.desc()).all()
    for post in posts:
        post.create_date = post.create_date.replace(tzinfo=from_zone).astimezone(to_zone)
        post.pub_date = post.pub_date.replace(tzinfo=from_zone).astimezone(to_zone)
    categories = Category.query.order_by(Category.name).all()
    return render_template('index.html',
                           active=active,
                           tweets=myTweets,
                           mentions=myMentions,
                           posts=posts,
                           categories=categories,
                           )


@app.route('/projects/')
def projects():
    active = 'projects'
    return render_template('projects.html',
                           active=active,
                           tweets=myTweets,
                           mentions=myMentions,
                           )


@app.route('/register/', methods=["GET", "POST"])
def register():
    form = RegisterForm(request.form)
    if form.validate_on_submit():
        if User.query.filter(func.lower(User.username) == func.lower(form.username.data)).first():
            flash('Username taken')
        elif User.query.filter(func.lower(User.email) == func.lower(form.email.data)).first():
            flash('Email already registered')
        else:
            activation_hash = get_activation_hash()
            user = User(first_name=form.first_name.data, last_name=form.last_name.data, username=form.username.data,
                        email=form.email.data, password=form.password.data, activation_hash=activation_hash)
            try:
                send_mail.send_activation_email(user.username, user.email, user.activation_hash)
                flash('Thanks for registering, your activation email has been sent to %s' % form.email.data)
            except mail.error:
                flash('Unable to send message!! Unable to register, try later!', category="error")
            db.session.add(user)
            db.session.commit()
            return redirect(url_for('index'))
    return render_template('register.html',
                           tweets=myTweets,
                           mentions=myMentions,
                           form=form,
                           )


@app.route('/activate_user/<activation_hash>')
def activate_user(activation_hash):
    """
    Activate user function.
    """
    user = User.query.filter_by(activation_hash=activation_hash).first_or_404()
    if user.status == 1:
        user.status = 2
        db.session.commit()
        send_mail.send_activation_successful_email(user)
        flash('user has been activated', 'info')
    elif user.status == 2:
        flash('user already activated', 'info')
    return redirect(url_for('index'))


@app.route("/login/", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated():
        return redirect(url_for('index'))

    form = LoginForm()
    if form.validate_on_submit():
        # login and validate the user...
        user = User.query.filter_by(username=form.username.data).first()
        if user is not None and user.check_password(form.password.data):
            if login_user(user, remember=form.remember.data):
                # Enable session expiration only if user hasn't chosen to be
                # remembered.
                session.permanent = not form.remember.data
                flash('Logged in successfully!', 'success')
                #flash(request.args.get('next'))
                return redirect(request.args.get('next') or url_for('index'))
            else:
                flash('This username is disabled!', 'error')
        else:
            flash('Wrong username or password!', 'error')
    return render_template('login.html',
                           tweets=myTweets,
                           mentions=myMentions,
                           form=form,
                           )


@app.route('/logout/')
@login_required
def logout():
    logout_user()
    flash('You have logged out!')
    return redirect(url_for('index'))