from .decorators import async
from flask import current_app, render_template
from flask_mail import Message
from app import mail


"""
@async
def send_async_email(msg):
    mail.send(msg)
"""

def send_email(subject, recipients, template, **kwargs):
    app = current_app._get_current_object()
    msg = Message(subject, sender = 'admin', recipients = recipients)
    msg.body = render_template(template + '.txt', **kwargs)
    msg.html = render_template(template + '.html', **kwargs)
    mail.send(msg)
