from celery import Celery
from flask_mail import Mail, Message
from flask import current_app, render_template
from os import environ
from edurange_refactored.settings import CELERY_BROKER_URL, CELERY_RESULT_BACKEND

import os

path_to_directory = os.path.dirname(os.path.abspath(__file__))


def get_path(file_name):
    mail_path = os.path.normpath(os.path.join(path_to_directory, 'templates/utils', file_name))
    return mail_path


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
    app.config.update(
        MAIL_SERVER='smtp.googlemail.com',
        MAIL_PORT=465,
        MAIL_USE_TLS=False,
        MAIL_USE_SSL=True
    )
    mail = Mail(app)
    msg = Message(email_data['subject'],
                  sender=environ.get('MAIL_DEFAULT_SENDER'),
                  recipients=[email_data['to']])
    mail.send(msg)
    msg.body = email_data['body']


@celery.task
def test_send_async_email(email_data):
    app = current_app
    mail = Mail(app)
    msg = Message(email_data['subject'],
                  sender=environ.get('MAIL_DEFAULT_SENDER'),
                  recipients=[email_data['email']])

    msg.body = render_template('utils/reset_password_email.txt', token=email_data['token']
                               , email=email_data['email'], _external=True)
    msg.html = render_template('utils/reset_password_email.html', token=email_data['token']
                               , email=email_data['email'], _external=True)
    mail.send(msg)

# @celery.task
# def start_scenario(scenario_data):
#     app = current_app
#     command = 'terraform apply -fy --config'
#     app.run(command)
