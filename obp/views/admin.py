__author__ = 'One Bad Panda'
from datetime import datetime
from flask import flash, render_template, Blueprint, request, redirect, url_for
from flask.ext.login import login_required, current_user
from obp import login_manager
from obp import db
from obp.constants import user as USER
from obp.constants import post as POST
from obp.forms.admin import categories, tags, posts, users
from obp.forms.admin import UserNew, UserEdit, PostNew, PostEdit
from obp.helpers.decorators import admin_required
from obp.models.User import User
from obp.models.Post import Post


admin = Blueprint('admin', __name__, url_prefix='/admin')


@admin.before_request
def staff_or_higher():
    if current_user.role is not USER.STAFF and current_user.role is not USER.ADMIN:
        return redirect(url_for('index'))


def delete_user(user_id):
    if current_user.id == user_id:
        message = "You can't delete yourself"
        message_type = "error"
    elif user_id == 0:
        message = "You can't delete the default admin"
        message_type = "error"
    else:
        user = User.query.filter_by(id=user_id).first()
        user_posts = Post.query.filter_by(user_id=user_id).all()
        for post in user_posts:
            post.user_id = 0
            post.status = POST.PENDING
            db.session.add(post)
            db.session.commit()
        db.session.delete(user)
        db.session.commit()
        message = "User: %s deleted, assigned posts to default admin user." % user.username
        message_type = "success"

    return message, message_type


def ban_user(user_id):
    if current_user.id == user_id:
        message = "You can't ban yourself"
        message_type = "error"
    else:
        user = User.query.filter_by(id=user_id).first()
        user.status = USER.BANNED
        db.session.commit()
        message = "User: %s banned" % user.username
        message_type = "success"
    return message, message_type


def unban_user(user_id):
    user = User.query.filter_by(id=user_id).first()
    user.status = USER.ACTIVE
    db.session.commit()
    message = "User: %s unbanned" % user.username
    message_type = "success"
    return message, message_type


def publish_post(post_id):
    post = Post.query.filter_by(id=post_id).first()
    post.status = POST.PUBLISHED
    if post.pub_date is None:
        post.pub_date = datetime.utcnow()
    db.session.add(post)
    db.session.commit()


def pend_post(post_id):
    post = Post.query.filter_by(id=post_id).first()
    post.status = POST.PENDING
    if post.pub_date is not None:
        post.pub_date = None
    db.session.add(post)
    db.session.commit()


def delete_post(post_id):
    post = Post.query.filter_by(id=post_id).first()
    db.session.delete(post)
    db.session.commit()


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


@admin.route('/')
@login_required
def index():
    return render_template('admin/index.html')


@admin.route('/users/', methods=["GET", "POST"])
@admin_required
@login_required
def user_index():
    users = User.query.order_by(User.username).all()
    user_ids = request.form.getlist("multi-action")

    if request.method == 'POST':
        action = request.form['action']
        for user_id in user_ids:
            user = User.query.filter_by(id=user_id).first()
            if action == "delete":
                result = delete_user(user.id)
                flash(result[0], category=result[1])
            if action == "ban":
                result = ban_user(user.id)
                flash(result[0], category=result[1])
            if action == "un-ban":
                result = unban_user(user.id)
                flash(result[0], category=result[1])
        return redirect(url_for('admin.user_index'))
    return render_template('admin/user_index.html',
                           users=users,
                           roles=USER,
                           user_role=USER.ROLE,
                           user_status=USER.STATUS,
                           )


@admin.route('/users/add', methods=["GET", "POST"])
@admin_required
@login_required
def user_add():
    form = UserNew()
    if form.validate_on_submit():
        if User.query.filter_by(username=form.username.data).first():
            flash('Username taken')
        if User.query.filter_by(email=form.email.data).first():
            flash('Email already registered')
        else:
            user = User(first_name=form.first_name.data,
                        last_name=form.last_name.data,
                        username=form.username.data,
                        email=form.email.data,
                        password=form.password.data,
                        role=form.role.data,
                        status=form.status.data)
            db.session.add(user)
            db.session.commit()

            flash('User %s added' % user.username)
            return redirect(url_for('admin.user_index'))
    return render_template('admin/edit.html',
                           form=form,
                           action="New",
                           data_type="User",
                           button_text="Save",
                           )


@admin.route('/users/edit/<int:user_id>/', methods=["GET", "POST"])
@admin_required
@login_required
def user_edit(user_id):
    user = User.query.filter_by(id=user_id).first()
    form = UserEdit(request.form, obj=user)
    if form.validate_on_submit():
        form.populate_obj(user)
        db.session.commit()
        flash("User %s updated" % user.username, category="success")
        #return redirect(url_for('admin.user_edit',user_id=user.id))
        return redirect(url_for('admin.user_index'))
    return render_template('admin/edit.html',
                           form=form,
                           action="Edit",
                           data_type="User",
                           button_text="Update",
                           )


@admin.route('/users/delete/<int:user_id>/', methods=["GET", "POST"])
@admin_required
@login_required
def user_delete(user_id):
    result = delete_user(user_id)
    flash(result[0], category=result[1])
    return redirect(url_for('admin.user_index'))


@admin.route('/users/ban/<int:user_id>/', methods=["GET", "POST"])
@login_required
def user_ban(user_id):
    result = ban_user(user_id)
    flash(result[0], category=result[1])
    return redirect(url_for('admin.user_index'))


@admin.route('/users/unban/<int:user_id>/', methods=["GET", "POST"])
@login_required
def user_unban(user_id):
    result = unban_user(user_id)
    flash(result[0], result[1])
    return redirect(url_for('admin.user_index'))


@admin.route('/posts/', methods=["GET", "POST"])
@login_required
def post_index():
    if current_user.role is not USER.ADMIN:
        posts = Post.query.filter_by(user_id=current_user.id).all()
    else:
        posts = Post.query.all()
    post_ids = request.form.getlist("multi-action")

    if request.method == 'POST':
        action = request.form['action']
        for post_id in post_ids:
            post = Post.query.filter_by(id=post_id).first()
            if action == "delete":
                delete_post(post.id)
                flash("Deleted post \"%s\"" % post.title, category="success")
            if action == "pend":
                pend_post(post.id)
                flash("Pended post \"%s\"" % post.title, category="success")
            if action == "publish":
                publish_post(post.id)
                flash("Published post \"%s\"" % post.title, category="success")
        return redirect(url_for('admin.post_index'))
    return render_template('admin/post_index.html',
                           posts=posts,
                           post_status=POST.STATUS,
                           categories=categories()
                           )


@admin.route('/posts/add', methods=["GET", "POST"])
@login_required
def post_add():
    form = PostNew()
    if form.validate_on_submit():
        if form.status.data == POST.PUBLISHED:
            pub_date = datetime.utcnow()
        else:
            pub_date = None
        post = Post(user_id=current_user.id,
                    title=form.title.data,
                    body=form.body.data,
                    category_id=form.category_id.data,
                    create_date=datetime.utcnow(),
                    pub_date=pub_date,
                    status=form.status.data)
        db.session.add(post)
        db.session.commit()

        flash('Post %s added' % post.title)
        return redirect(url_for('admin.post_index'))
    return render_template('admin/edit.html',
                           form=form,
                           action="New",
                           data_type="Post",
                           button_text="Save",
                           )


@admin.route('/posts/edit/<int:post_id>/', methods=["GET", "POST"])
@login_required
def post_edit(post_id):
    post = Post.query.filter_by(id=post_id).first()
    form = PostEdit(request.form, obj=post)
    if form.validate_on_submit():
        form.populate_obj(post)
        if form.status.data is not POST.PUBLISHED:
            post.pub_date = None
        else:
            post.pub_date = datetime.utcnow()
        db.session.commit()
        flash("Post: \"%s\"  updated" % post.title, category="success")
        #return redirect(url_for('admin.user_edit',user_id=user.id))
        return redirect(url_for('admin.post_index'))
    return render_template('admin/edit.html',
                           form=form,
                           action="Edit",
                           data_type="Post",
                           button_text="Update",
                           )