# -*- coding: utf-8 -*-
"""The app module, containing the app factory function."""
import logging
import sys

from flask import Flask, render_template

from edurange_refactored import commands, public, user, tutorials
from edurange_refactored.extensions import (
    bcrypt,
    cache,
    csrf_protect,
    db,
    debug_toolbar,
    flask_static_digest,
    login_manager,
    migrate,
)
from edurange_refactored.user.models import Scenarios
from edurange_refactored.tasks import stop


def create_app(config_object="edurange_refactored.settings"):
    """Create application factory, as explained here: http://flask.pocoo.org/docs/patterns/appfactories/.

    :param config_object: The configuration object to use.
    """
    app = Flask(__name__.split(".")[0])
    app.config.from_object(config_object)
    register_extensions(app)
    register_blueprints(app)
    register_errorhandlers(app)
    register_shellcontext(app)
    register_commands(app)
    configure_logger(app)

    sync_docker(app)

    return app


def register_extensions(app):
    """Register Flask extensions."""
    bcrypt.init_app(app)
    cache.init_app(app)
    db.init_app(app)
    csrf_protect.init_app(app)
    login_manager.init_app(app)
    debug_toolbar.init_app(app)
    migrate.init_app(app, db)
    flask_static_digest.init_app(app)
    return None


def register_blueprints(app):
    """Register Flask blueprints."""
    app.register_blueprint(public.views.blueprint)
    app.register_blueprint(user.views.blueprint)
    app.register_blueprint(tutorials.views.blueprint)
    return None


def register_errorhandlers(app):
    """Register error handlers."""

    def render_error(error):
        """Render error template."""
        # If a HTTPException, pull the `code` attribute; default to 500
        error_code = getattr(error, "code", 500)
        return (
            render_template(f"{error_code}.html"),
            error_code,
        )  # removed f from render_template(f...

    for errcode in [401, 403, 404, 500]:
        app.errorhandler(errcode)(render_error)
    return None


def register_shellcontext(app):
    """Register shell context objects."""

    def shell_context():
        """Shell context objects."""
        return {"db": db, "User": user.models.User}

    app.shell_context_processor(shell_context)


def register_commands(app):
    """Register Click commands."""
    app.cli.add_command(commands.test)
    app.cli.add_command(commands.lint)


def configure_logger(app):
    """Configure loggers."""
    handler = logging.StreamHandler(sys.stdout)
    if not app.logger.handlers:
        app.logger.addHandler(handler)


# TODO this got longer than expected. can it fit better somewhere else? tasks.py?
def sync_docker(app):
    """Synchronize the state of the Docker daemon active containers
    with the database/what Flask shows on the scenarios page.

    Execution flow:
    - iterate through the folders in data/tmp/
    - extract name of the docker containers/networks using `terraform state list`
        docker_container.sname_nat OR docker_network.sname_NAT/PLAYER
    -
    """
    import docker
    import os
    import subprocess

    # get a list of scenarios in database
    init_dir = os.getcwd() # preserve initial dir
    tmp_root = os.environ['EDURANGE_HOME'] + '/data/tmp/'
    os.chdir(tmp_root)

    # iterate over scenario folders and get terraform states
    tf_containers = set()
    for folder in os.listdir():
        if folder == 'plugin_cache':
            # skip plugin cache
            continue
        os.chdir(tmp_root + folder) # chdir to scenario folder

        # verify that folder contains a .tfstate file (has been started)
        if any('tfstate' in file for file in os.listdir()):
            tf_state = subprocess.run(['terraform', 'state', 'list'], capture_output=True, text=True)

            # split stdout from above command by '\n' char
            # leave off last item (always '')
            # iterate across list and get containers (exclude networks)
            tmp = [name.split('.')[-1].split('_')[0] for name in tf_state.stdout.split('\n')[:-1] if 'docker_container' in name]
            for name in tmp:
                tf_containers.add(name)
            continue
    # reset to initial working dir
    os.chdir(init_dir)
    # DEBUG
    # print('containers only:', tf_containers)
    # print('tf containers/networks:\n', tf_objects)

    # get active containers from docker
    try:
        client = docker.from_env()
        docker_containers = client.containers.list()
        docker_containers = set([c.name.split('_')[0] for c in docker_containers])
        # print()
        # print('docker containers:', docker_containers)
    except:
        # print("docker section error")
        pass


    # get update db to match docker
    # try:
    with app.app_context():
        scenarios_in_db = Scenarios.query.all()
        # print()
        db_scenario_dict = dict((s.name.replace('_',''), s) for s in scenarios_in_db if s.status == 1)
        # print("scenarios in db:", db_scenario_dict)
        db_scenario_set = set(db_scenario_dict.keys())
        db_docker_diff = db_scenario_set.difference(docker_containers)
        # print('db set diff docker set', db_docker_diff)
        for s in db_docker_diff:
            init_dir = os.getcwd()
            os.chdir(os.environ['EDURANGE_HOME'] + '/data/tmp/'+ s)
            os.system('terraform destroy --auto-approve')
            db_scenario_dict[s].update(status=0)
            os.chdir(init_dir)


    # except:
    #     # send message to celery saying there are no scenarios
    #     pass
