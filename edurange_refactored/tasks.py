import json
import os
import random
import shutil
import string
import subprocess
from datetime import datetime
from os import environ

from celery import Celery
from celery.utils.log import get_task_logger
from flask import current_app, flash, render_template
from flask_mail import Mail, Message

from edurange_refactored.scenario_json import adjust_network, find_and_copy_template, write_resource
from edurange_refactored.scenario_utils import gather_files
from edurange_refactored.settings import CELERY_BROKER_URL, CELERY_RESULT_BACKEND

logger = get_task_logger(__name__)

path_to_directory = os.path.dirname(os.path.abspath(__file__))


def get_path(file_name):
    mail_path = os.path.normpath(
        os.path.join(path_to_directory, "templates/utils", file_name)
    )

    return mail_path


celery = Celery(__name__, broker=CELERY_BROKER_URL, backend=CELERY_RESULT_BACKEND)


class ContextTask(celery.Task):
    ''' This allows tasks to assume the create_app() context, and access the database '''
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
        MAIL_SERVER="smtp.googlemail.com",
        MAIL_PORT=465,
        MAIL_USE_TLS=False,
        MAIL_USE_SSL=True,
    )
    mail = Mail(app)
    msg = Message(
        email_data["subject"],
        sender=environ.get("MAIL_DEFAULT_SENDER"),
        recipients=[email_data["to"]],
    )
    mail.send(msg)
    msg.body = email_data["body"]


@celery.task
def test_send_async_email(email_data):
    app = current_app
    mail = Mail(app)
    msg = Message(
        email_data["subject"],
        sender=environ.get("MAIL_DEFAULT_SENDER"),
        recipients=[email_data["email"]],
    )

    msg.body = render_template(
        "utils/reset_password_email.txt",
        token=email_data["token"],
        email=email_data["email"],
        _external=True,
    )
    msg.html = render_template(
        "utils/reset_password_email.html",
        token=email_data["token"],
        email=email_data["email"],
        _external=True,
    )
    mail.send(msg)


@celery.task(bind=True)
def CreateScenarioTask(self, name, s_type, owner, group, g_id, s_id, namedict):
    ''' self is the task instance, other arguments are the results of database queries '''
    from edurange_refactored.user.models import ScenarioGroups, Scenarios

    app = current_app
    s_type = s_type.lower()
    g_id = g_id["id"]

    c_names, g_files, s_files, u_files, packages, ip_addrs = gather_files(s_type, logger)

    logger.info(
        "Executing task id {0.id}, args: {0.args!r} kwargs: {0.kwargs!r}".format(
            self.request
        )
    )

    students = {}
    usernames, passwords = [], []

    for i in range(len(group)):
        username = "".join(e for e in group[i]["username"] if e.isalnum())
        password = "".join(
            random.choice(string.ascii_letters + string.digits) for _ in range(6)
        )

        usernames.append(username)
        passwords.append(password)

        logger.info(f'User: {group[i]["username"]}')
        students[username] = []
        students[username].append({"username": username, "password": password})

    logger.info("All names: {}".format(students))

    with app.test_request_context():
        scenario = Scenarios.query.filter_by(id=s_id).first()
        name = "".join(e for e in name if e.isalnum())

        os.makedirs("./data/tmp/" + name)
        os.chdir("./data/tmp/" + name)

        os.makedirs("./student_view")

        with open("students.json", "w") as outfile:
            json.dump(students, outfile)

        # create file of chat names for the scenario
        with open(f"../chatnames.json", "w") as chatnamefile:
           json.dump(namedict, chatnamefile)

        questions = open(f"../../../scenarios/prod/{s_type}/questions.yml", "r+")
        content = open(f"../../../scenarios/prod/{s_type}/student_view/content.json", "r+")

        logger.info(f"Questions Type: {type(questions)}")
        logger.info(f"Content Type: {type(content)}")

        flags = []
        if s_type == "getting_started" or s_type == "file_wrangler":
            flags.append("".join(random.choice(string.ascii_letters + string.digits) for _ in range(8)))
            flags.append("".join(random.choice(string.ascii_letters + string.digits) for _ in range(8)))

            questions = questions.read().replace("$RANDOM_ONE", flags[0]).replace("$RANDOM_TWO", flags[1])
            content = content.read().replace("$RANDOM_ONE", flags[0]).replace("$RANDOM_TWO", flags[1])

        with open("questions.yml", "w") as outfile:
            if type(questions) == str:
                outfile.write(questions)
            else:
                outfile.write(questions.read())

        with open("./student_view/content.json", "w") as outfile:
            if type(content) == str:
                outfile.write(content)
            else:
                outfile.write(content.read())

        active_scenarios = Scenarios.query.count()
        starting_octet = int(os.getenv("SUBNET_STARTING_OCTET", 10))

        # Local addresses begin at the subnet 10.0.0.0/24
        address = str(starting_octet + active_scenarios)

        # Write provider and networks
        find_and_copy_template(s_type, "network")
        adjust_network(address, name)
        os.system("terraform init")
        os.system("terraform plan -out network")

        logger.info("All flags: {}".format(flags))

        # Each container and their names are pulled from the 's_type'.json file
        for i, c in enumerate(c_names):
            find_and_copy_template(s_type, c)
            write_resource(
                address, name, s_type, c_names[i], usernames, passwords,
                s_files[i], g_files[i], u_files[i], flags
            )

        scenario.update(
            status=0,
            subnet=f"{address}.0.0.0/27"
        )
        os.chdir("../../..")

        ScenarioGroups.create(group_id=g_id, scenario_id=s_id)


@celery.task(bind=True)
def start(self, sid):
    from edurange_refactored.user.models import Scenarios
    from edurange_refactored.utils import setAttempt
    from edurange_refactored.notification_utils import NotifyCapture

    app = current_app
    logger.info(
        "Executing task id {0.id}, args: {0.args!r} kwargs: {0.kwargs!r}".format(
            self.request
        )
    )
    with app.test_request_context():
        scenario = Scenarios.query.filter_by(id=sid).first()
        logger.info("Found Scenario: {}".format(scenario))
        name = str(scenario.name)
        name = "".join(e for e in name if e.isalnum())
        if int(scenario.status) != 0:
            logger.info("Invalid Status")
            NotifyCapture("Failed to start scenario " + name + ": Invalid Status")
            raise Exception(f"Scenario must be stopped before starting")
        elif os.path.isdir(os.path.join("./data/tmp/", name)):
            scenario.update(status=3)
            logger.info("Folder Found")
            os.chdir("./data/tmp/" + name)
            os.system("terraform apply network")
            os.system("terraform apply --auto-approve")
            os.chdir("../../..")
            scenario.update(status=1)
            scenario.update(attempt=setAttempt(sid))
            NotifyCapture("Scenario " + name + " has started successfully.")
        else:
            #part that Jack discussed about
            logger.info("Scenario folder could not be found -- " + os.path.join("./data/tmp/", name))
            NotifyCapture("Failed to start scenario " + name + ": Scenario folder could not be found. -- " + os.path.join("./data/tmp/", name))
            flash("Scenario folder could not be found")

#function for grabbing notify could be made (already made in separate utils file for notification)

@celery.task(bind=True)
def stop(self, sid):
    from edurange_refactored.user.models import Scenarios
    from edurange_refactored.notification_utils import NotifyCapture

    app = current_app
    logger.info(
        "Executing task id {0.id}, args: {0.args!r} kwargs: {0.kwargs!r}".format(
            self.request
        )
    )
    with app.test_request_context():
        scenario = Scenarios.query.filter_by(id=sid).first()
        logger.info("Found Scenario: {}".format(scenario))
        name = str(scenario.name)
        name = "".join(e for e in name if e.isalnum())
        if int(scenario.status) != 1:
            logger.info("Invalid Status")
            NotifyCapture("Failed to stop scenario " + name + ": Invalid Status")
            flash("Scenario is not ready to start", "warning")
        elif os.path.isdir(os.path.join("./data/tmp/", name)):
            logger.info("Folder Found")
            scenario.update(status=4)
            os.chdir("./data/tmp/" + name)
            os.system("terraform destroy --auto-approve")
            os.chdir("../../..")
            scenario.update(status=0)
            NotifyCapture("Scenario " + name + " has successfully stopped.")
        else:
            logger.info("Something went wrong")
            NotifyCapture("Failed to stop scenario " + name + ": Invalid Status")
            flash("Something went wrong", "warning")


@celery.task(bind=True)
def destroy(self, sid):
    from edurange_refactored.user.models import Scenarios, ScenarioGroups, Responses
    from edurange_refactored.notification_utils import NotifyCapture

    app = current_app
    logger.info(
        "Executing task id {0.id}, args: {0.args!r} kwargs: {0.kwargs!r}".format(
            self.request
        )
    )
    with app.test_request_context():
        scenario = Scenarios.query.filter_by(id=sid).first()
        if scenario is not None:
            logger.info("Found Scenario: {}".format(scenario))
            name = str(scenario.name)
            name = "".join(e for e in name if e.isalnum())
            s_id = str(scenario.id)
            s_group = ScenarioGroups.query.filter_by(scenario_id=s_id).first()
            if int(scenario.status) != 0:
                logger.info("Invalid Status")
                NotifyCapture("Failed to delete scenario" + name + ": Invalid Status")
                raise Exception(f"Scenario in an Invalid state for Destruction")
            s_responses = Responses.query.filter_by(scenario_id=s_id).all()
            for r in s_responses:
                r.delete()
            if os.path.isdir(os.path.join("./data/tmp/", name)):
                logger.info("Folder Found, current directory: {}".format(os.getcwd()))
                os.chdir("./data/tmp/")
                shutil.rmtree(name)
                os.chdir("../..")
                if s_group:
                    s_group.delete()
                scenario.delete()
                NotifyCapture("The Scenario " + name + " is successfully deleted.")
            else:
                logger.info("Scenario files not found, assuming broken scenario and deleting")
                NotifyCapture("Failed to delete scenario " + name + ": Scenario files could not be found.")
                scenario.delete()
        else:
            NotifyCapture("Failed to delete scenario " + name + ": Scenario could not be found.")
            raise Exception(f"Could not find scenario")

#global scenarios_dict
scenarios_dict = {}
@celery.task(bind=True)
#def scenarioTimeoutWarningEmail(self):
def scenarioTimeoutWarningEmail(self, arg):
    from edurange_refactored.user.models import Scenarios
    from edurange_refactored.user.models import User
    scenarios = Scenarios.query.all()
    users = User.query.all()
    global scenarios_dict
    for scenario in scenarios:
        for user in users:
            if scenario.id in scenarios_dict.keys() == False:
                scenarios_dict = {scenario.id : scenario.status}
            elif scenario.id in scenarios_dict.keys() and scenarios_dict[scenario.id] == 1 and scenario.status == 1:
                if user.id == scenario.owner_id:
                    email = user.email
                    email_data = {"subject": "WARNING: Scenario Running Too Long", "email": email}
                    app = current_app
                    mail = Mail(app)
                    msg = Message(email_data['subject'],
                                sender=environ.get('MAIL_DEFAULT_SENDER'),
                                recipients=[email_data['email']])
                    msg.body = render_template('utils/scenario_timeout_warning_email.txt', email=email_data['email'], _external=True)
                    msg.html = render_template('utils/scenario_timeout_warning_email.html', email=email_data['email'], _external=True)
                    mail.send(msg)
            scenarios_dict[scenario.id] = scenario.status
    #    print(arg)
    #email_data = {'subject': 'WARNING: Scenario Running Too Long', 'to': 'selenawalshsmith@gmail.com', 'body':'WARNING: Scenario Running Too Long'}
    #send_async_email(email_data)


@celery.task(bind=True)
def scenarioCollectLogs(self, arg):
    from edurange_refactored.csv_utils import readCSV
    from edurange_refactored.extensions import db
    from edurange_refactored.user.models import BashHistory

    def get_or_create(session, model, **kwargs):
        instance = session.query(model).filter_by(**kwargs).first()
        if instance:
            return instance
        else:
            instance = model(**kwargs)
            session.add(instance)
            session.commit()
            return instance

    containers = subprocess.run(['docker', 'container', 'ls'], stdout=subprocess.PIPE).stdout.decode('utf-8')
    containers = containers.split('\n')
    scenarios = []
    for i, c in enumerate(containers[:-1]):
        if i == 0:
            continue
        c = c.split(' ')
        c_name = c[-1]
        if c_name is not None and c_name != 'ago' and c_name != 'NAMES':
            if c_name.split('_')[0] is not None and c_name.split('_')[0] not in scenarios:
                scenarios.append(c_name.split('_')[0])
        try:  # This is dangerous, may want to substitute for subprocess.call
            os.system(f'docker cp {c_name}:/usr/local/src/merged_logs.csv logs/{c_name}.csv')
            os.system(f'docker cp {c_name}:/usr/local/src/raw_logs.zip logs/{c_name}.zip')
        except FileNotFoundError as e:
            print(f'{e}')

    files = subprocess.run(['ls', 'logs/'], stdout=subprocess.PIPE).stdout.decode('utf-8')
    files = files.split('\n')[:-1]
    for s in scenarios:
        if os.path.isdir(f'data/tmp/{s}'):
            try:
                os.system(f'cat /dev/null > data/tmp/{s}/{s}-history.csv')
            except Exception as e:
                print(f'Not a scenario: {e} - Skipping')

    for f in files:
        for s in scenarios:
            if f.find(s) == 0 and os.path.isdir(f'data/tmp/{s}') and f.endswith('.csv'):
                try:
                    os.system(f'cat logs/{f} >> data/tmp/{s}/{s}-history.csv')
                except Exception as e:
                    print(f'Not a scenario: {e} - Skipping')
            if f.find(s) == 0 and os.path.isdir(f'data/tmp/{s}') and f.endswith('.zip'):
                try:
                    os.system(f'cp logs/{f} data/tmp/{s}/{s}-raw.zip')
                except Exception as e:
                    print(f'Not a scenario: {e} - Skipping')

    for s in scenarios:
        try:
            data = readCSV(s, 'name')
            for i, line in enumerate(data):
                if i == 0:
                    continue
                line[3] = datetime.fromtimestamp(int(line[3]))

                get_or_create(
                    session=db.session,
                    model=BashHistory,
                    scenario_name=s,
                    container_name=line[6].split(':')[0],
                    timestamp=line[3],
                    current_directory=line[5],
                    input=line[6].split(':')[-1],
                    output=line[6],
                    prompt=line[1]
                )
        except FileNotFoundError as e:
            print(f"Container not found: {e} - Skipping")


@celery.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    # 21600 is 6 hrs in seconds
    sender.add_periodic_task(21600.0, scenarioTimeoutWarningEmail.s(''))
    sender.add_periodic_task(60.0, scenarioCollectLogs.s(''))
