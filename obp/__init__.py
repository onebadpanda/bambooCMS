from obp.helpers import config

__author__ = 'One Bad Panda'
from flask import Flask
from flask.ext.bootstrap import Bootstrap
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager
from flask.ext.bcrypt import Bcrypt
from flask.ext.mail import Mail


app = Flask(__name__)

app.config.from_object(config.DevelopmentConfig)
Bootstrap(app)
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
mail = Mail(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = '/login'

from obp.views.admin import admin as adminModule
app.register_blueprint(adminModule)
