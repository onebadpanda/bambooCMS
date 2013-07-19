__author__ = 'One Bad Panda'
from flask import url_for
from flask.ext.mail import Message
from obp import mail as mailer


def send_activation_email(username, email, activation_hash):
    """
    Send the awaiting for confirmation mail to the user.
    """
    subject = ""
    confirmation_url = url_for('activate_user', activation_hash=activation_hash, _external=True)
    body = "Dear %s, click here to confirm: %s" % (username, confirmation_url)
    reply_to = ''
    mail_to_be_sent = Message(subject=subject, recipients=[email], body=body, reply_to=reply_to)
    mailer.send(mail_to_be_sent)

def send_activation_successful_email(user):
    """
    Send the awaiting for confirmation mail to the user.
    """
    subject = ""
    login_url = url_for('login', _external=True)
    body = "Dear %s, your account has been activated you can login at: %s" % (user.username, login_url)
    reply_to = ''
    mail_to_be_sent = Message(subject=subject, recipients=[user.email], body=body, reply_to=reply_to)
    mailer.send(mail_to_be_sent)