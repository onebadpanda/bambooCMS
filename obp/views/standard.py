__author__ = 'One Bad Panda'
import base64
import hashlib
import logging
import random
import re
from datetime import datetime
from dateutil import tz
from markdown import markdown
from flask import Markup
from flask import flash, render_template, redirect, request, session, url_for
from flask.ext.login import current_user, login_user, login_required, logout_user
from sqlalchemy import func
from werkzeug.contrib.cache import SimpleCache
from obp import app, db, mail
from obp.constants import post as post_status
from obp.forms.standard import RegisterForm, LoginForm, CommentForm
from obp.helpers import send_mail
from obp.helpers import tweets
from obp.models.User import User
from obp.models.Post import Post
from obp.models.Category import Category
from obp.models.Comment import Comment
from obp.models.Tag import Tag

from_zone = tz.gettz('UTC')
to_zone = tz.tzlocal()

cache = SimpleCache()


def get_activation_hash():
    result = base64.b64encode(hashlib.sha256(str(random.getrandbits(256))).digest(),
                              random.choice(['rA', 'aZ', 'gQ', 'hH', 'hG', 'aR', 'DD'])).rstrip('==')
    return result


def get_all_mentions():
    rv = cache.get('my_latest_mentions')
    if rv is None:
        rv = tweets.get_latest_mentions()
        cache.set('my_latest_mentions', rv, timeout=15 * 60)
    return rv


def get_all_tweets():
    rv = cache.get('my_latest_tweets')
    if rv is None:
        rv = tweets.get_latest_tweets()
        cache.set('my_latest_tweets', rv, timeout=15 * 60)
    return rv


def get_all_categories():
    return Category.query.order_by(Category.name).all()


def get_all_tags():
    return Tag.query.order_by(Tag.name).all()


@app.template_filter('markdown')
def markdown_filter(data):
    return Markup(markdown(data))


@app.template_filter('twitterize')
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


@app.errorhandler(404)
def page_not_found(error):
    return render_template('page_not_found.html', error=404)


app.jinja_env.globals.update(
    tweets=get_all_tweets(),
    mentions=get_all_mentions(),
    categories=get_all_categories(),
    tags=get_all_tags()
)


@app.route('/')
def index():
    active = 'blog'
    posts = Post.query.filter_by(status=post_status.PUBLISHED).order_by(Post.pub_date.desc()).all()
    for post in posts:
        post.create_date = post.create_date.replace(tzinfo=from_zone).astimezone(to_zone)
        post.pub_date = post.pub_date.replace(tzinfo=from_zone).astimezone(to_zone)
    return render_template('index.html', active=active, posts=posts)


@app.route('/projects/')
def projects():
    active = 'projects'
    return render_template('projects.html', active=active)


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
    return render_template('register.html',form=form)


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
    return render_template('login.html', form=form)


@app.route('/logout/')
@login_required
def logout():
    logout_user()
    flash('You have logged out!')
    return redirect(url_for('index'))


@app.route('/posts/<string:post_slug>/', methods=["GET", "POST"])
def individual_post(post_slug):
    post = Post.query.filter_by(slug=post_slug).first_or_404()
    post.pub_date = post.pub_date.replace(tzinfo=from_zone).astimezone(to_zone)

    form = CommentForm()
    comments = Comment.query.filter_by(post_id=post.id).order_by(Comment.id.asc()).all()

    if form.validate_on_submit() and current_user.is_authenticated():
        new_comment = Comment(user_id=current_user.id,
                              post_id=post.id,
                              create_date=datetime.utcnow(),
                              body=form.body.data,
                              )
        db.session.add(new_comment)
        db.session.commit()

        flash("Your comment has been added", category="success")
        return redirect(url_for('individual_post', post_slug=post_slug))
    for comment in comments:
        comment.create_date = comment.create_date.replace(tzinfo=from_zone).astimezone(to_zone)

    return render_template('post.html', form=form, post=post, comments=comments, button_text="Save")


@app.route('/categories/<string:category_slug>')
def category_index(category_slug):
    category = Category.query.filter_by(slug=category_slug).first_or_404()
    posts = Post.query.filter_by(category_id=category.id).all()

    return render_template('category.html', posts=posts, category=category)


@app.route('/tagged/<string:tag_slug>')
def tag_index(tag_slug):
    tag = Tag.query.filter_by(slug=tag_slug).first_or_404()
    posts = Post.query.filter(Post.tags.any(id=tag.id)).all()

    return render_template('tag.html', posts=posts, tag=tag)