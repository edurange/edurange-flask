from celery import Celery
from flask_mail import Mail, Message
from flask import current_app
from os import environ
from edurange_refactored.settings import CELERY_BROKER_URL, CELERY_RESULT_BACKEND
celery = Celery(__name__)
celery = Celery('tasks', broker=CELERY_BROKER_URL)
celery.conf.update({'CELERY_RESULT_BACKEND': CELERY_RESULT_BACKEND})


class ContextTask(celery.Task):
    abstract = True

    def __call__(self, *args, **kwargs):
        from edurange_refactored.app import create_app
        with create_app().app_context():
            return super(ContextTask, self).__call__(*args, **kwargs)


celery.Task = ContextTask


@celery.task
def send_async_email(email_data):
    app = current_app
    mail = Mail(app)
    msg = Message(email_data['subject'],
                  sender=environ.get('MAIL_DEFAULT_SENDER'),
                  recipients=[email_data['to']])
    msg.body = email_data['body']
    mail.send(msg)
