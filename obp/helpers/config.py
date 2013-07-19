__author__ = 'One Bad Panda'


class Config(object):
    DEBUG = False
    TESTING = False
    DATABASE_URI = 'sqlite://:memory:'

    #boostrap options
    BOOTSTRAP_FONTAWESOME = True
    BOOTSTRAP_USE_MINIFIED = True
    BOOTSTRAP_JQUERY_VERSION = '1.10.1'
    BOOTSTRAP_HTML5_SHIM = True

    #recaptcha options, used for registration
    RECAPTCHA_PUBLIC_KEY = ''
    RECAPTCHA_PRIVATE_KEY = ''
    RECAPTCHA_OPTIONS = {'theme': 'white',
                         }

    #twitter options, used for recent tweets and mentions
    TWITTER_CONSUMER_KEY = ''
    TWITTER_CONSUMER_SECRET = ''
    TWITTER_ACCESS_TOKEN_KEY = ''
    TWITTER_ACCESS_TOKEN_SECRET = ''
    TWITTER_USERNAME = ''

    #flask-mail settings, used for sending account emails
    MAIL_SERVER = ''
    MAIL_PORT = 25
    MAIL_USE_TLS = False
    MAIL_USE_SSL = False
    MAIL_DEBUG = False
    MAIL_USERNAME = ''
    MAIL_PASSWORD = ''
    MAIL_DEFAULT_SENDER = ''
    MAIL_DEFAULT_REPLY_TO = ''
    MAIL_MAX_EMAILS = 10
    MAIL_SUPPRESS_SEND = False


class ProductionConfig(Config):
    DATABASE_URI = 'mysql://user@localhost/foo'


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = ''
    SECRET_KEY = ''
    MAIL_DEBUG = True


class TestingConfig(Config):
    TESTING = True
    MAIL_SUPPRESS_SEND = True