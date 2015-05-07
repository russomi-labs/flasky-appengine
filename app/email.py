from threading import Thread

from flask import current_app, render_template
from flask.ext.mail import Message
from . import mail


def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)


def _send_email(to, subject, template, **kwargs):
    app = current_app._get_current_object()
    msg = Message(app.config['FLASKY_MAIL_SUBJECT_PREFIX'] + ' ' + subject,
                  sender=app.config['FLASKY_MAIL_SENDER'], recipients=[to])
    msg.body = render_template(template + '.txt', **kwargs)
    msg.html = render_template(template + '.html', **kwargs)
    thr = Thread(target=send_async_email, args=[app, msg])
    thr.start()
    return thr


def _send_email_gae(to, subject, template, **kwargs):
    from google.appengine.api import mail

    app = current_app._get_current_object()
    msg = mail.EmailMessage(sender=app.config['FLASKY_MAIL_SENDER'],
                            subject=app.config['FLASKY_MAIL_SUBJECT_PREFIX'] + ' ' + subject)
    msg.to = to
    msg.body = render_template(template + '.txt', **kwargs)
    msg.html = render_template(template + '.html', **kwargs)

    msg.send()


def send_email(to, subject, template, **kwargs):
    app = current_app._get_current_object()

    if app.config['MAIL_USE_GAE']:
        return _send_email_gae(to, subject, template, **kwargs)
    else:
        return _send_email(to, subject, template, **kwargs)
