__author__ = 'One Bad Panda'
from functools import wraps
from flask.ext.login import current_user, current_app
from obp.constants import user as role


def admin_required(func):
    @wraps(func)
    def decorated_view(*args, **kwargs):
        if current_user.role is not role.ADMIN:
            return current_app.login_manager.insufficient()
        return func(*args, **kwargs)
    return decorated_view