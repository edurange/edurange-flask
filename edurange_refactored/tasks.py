import shutil

from celery import Celery
from flask_mail import Mail, Message
from flask import current_app, render_template, session, flash
from os import environ
from edurange_refactored.settings import CELERY_BROKER_URL, CELERY_RESULT_BACKEND

import os
from celery.utils.log import get_task_logger

logger = get_task_logger(__name__)

path_to_directory = os.path.dirname(os.path.abspath(__file__))


def get_path(file_name):
    mail_path = os.path.normpath(os.path.join(path_to_directory, 'templates/utils', file_name))
    return mail_path


celery = Celery(__name__,
                broker=CELERY_BROKER_URL,
                backend=CELERY_RESULT_BACKEND)


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

@celery.task(bind=True)
def CreateScenarioTask(self, name, infoFile, owner, students):
    from edurange_refactored.user.models import Scenarios
    app = current_app
    logger.info('Executing task id {0.id}, args: {0.args!r} kwargs: {0.kwargs!r}'.format(
        self.request))
    with app.test_request_context():
        name = ''.join(e for e in name if e.isalnum())
        desc = 'Foo'
        own_id = owner
        Scenarios.create(name=name, description=desc, owner_id=own_id)

        os.mkdir('./data/tmp/' + name)
        os.chdir('./data/tmp/' + name)

        #copy_directory('scenarios/templates/' + SELECTION, os.curdir)

        with open('example.tf', 'w') as f:
            f.write("""provider "docker" {}
    provider "template" {}
    
    resource "docker_container" """ + "\""+ name + "\"" """ {
      name = """ + "\""+ name + "\"" """
      image = "rastasheep/ubuntu-sshd:18.04"
      restart = "always"
      hostname  = "NAT"
    
      connection {
        host = self.ip_address  
        type = "ssh"
        user = "root"
        password = "root"
      }
    
      ports {
        internal = 22
      }
    
      provisioner "remote-exec" {
        inline = [
        "useradd --home-dir /home/jack --create-home --shell /bin/bash --password $(echo passwordfoo | openssl passwd -1 -stdin) jack",
        ]
      }
    }""")
        os.system('terraform init')
        os.chdir('../../..')


@celery.task(bind=True)
def start(self, sid):
    from edurange_refactored.user.models import Scenarios
    app = current_app
    logger.info('Executing task id {0.id}, args: {0.args!r} kwargs: {0.kwargs!r}'.format(
        self.request))
    with app.test_request_context():
        scenario = Scenarios.query.filter_by(id=sid).first()
        logger.info('Found Scenario: {}'.format(scenario))
        name = str(scenario.name)
        if int(scenario.status) != 0:
            logger.info('Invalid Status')
            flash('Scenario is not ready to start', 'warning')
        elif os.path.isdir(os.path.join('./data/tmp/', name)):
            logger.info('Folder Found')
            scenario.update(status=1)
            os.chdir('./data/tmp/' + name)
            os.system('terraform apply --auto-approve')
            os.chdir('../../..')
        else:
            logger.info('Something went wrong')
            flash('Something went wrong', 'warning')

@celery.task(bind=True)
def stop(self, sid):
    from edurange_refactored.user.models import Scenarios
    app = current_app
    logger.info('Executing task id {0.id}, args: {0.args!r} kwargs: {0.kwargs!r}'.format(
        self.request))
    with app.test_request_context():
        scenario = Scenarios.query.filter_by(id=sid).first()
        logger.info('Found Scenario: {}'.format(scenario))
        name = str(scenario.name)
        if int(scenario.status) != 1:
            logger.info('Invalid Status')
            flash('Scenario is not ready to start', 'warning')
        elif os.path.isdir(os.path.join('./data/tmp/', name)):
            logger.info('Folder Found')
            os.chdir('./data/tmp/' + name)
            os.system('terraform destroy --auto-approve')
            scenario.update(status=0)
            os.chdir('../../..')
        else:
            logger.info('Something went wrong')
            flash('Something went wrong', 'warning')

@celery.task(bind=True)
def destroy(self, sid):
    from edurange_refactored.user.models import Scenarios
    app = current_app
    logger.info('Executing task id {0.id}, args: {0.args!r} kwargs: {0.kwargs!r}'.format(
        self.request))
    with app.test_request_context():
        scenario = Scenarios.query.filter_by(id=sid).first()
        logger.info('Found Scenario: {}'.format(scenario))
        name = str(scenario.name)
        if int(scenario.status) != 0:
            logger.info('Invalid Status')
            flash('Scenario must be stopped to destroy', 'warning')
        elif os.path.isdir(os.path.join('./data/tmp/', name)):
            logger.info('Folder Found, current directory: {}'.format(os.getcwd()))
            os.chdir('./data/tmp/')
            shutil.rmtree(name)
            os.chdir('../..')
            scenario.delete()
        else:
            logger.info('Something went wrong')
            flash('Something went wrong', 'warning')

