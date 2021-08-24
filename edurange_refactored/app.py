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
from edurange_refactored.user.models import User, Scenarios


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
    init_dir = os.getcwd() # preserve starting dir
    tmp_root = os.environ['EDURANGE_HOME'] + '/data/tmp/'
    os.chdir(tmp_root)

    # iterate over scenario folders and get terraform states
    tf_objects = []
    for folder in os.listdir():
        if folder == 'plugin_cache':
            continue
        os.chdir(tmp_root + folder) # chdir to scenario folder

        # skip scenario folders that do not contain a .tfstate file (never been started)
        previously_started = any('tfstate' in file for file in os.listdir())
        if previously_started:
            # print(folder)
            tf_state = subprocess.run(['terraform', 'state', 'list'], capture_output=True, text=True)

            # print(tf_state)
            tf_objects += [name.split('.')[-1] for name in tf_state.stdout.split('\n')[:-1]]
            continue
    print('tf containers/networks:')
    print(tf_objects)

    # reset cwd
    os.chdir(init_dir)

    # get active containers from docker 
    try:
        client = docker.from_env()
        running_containers = client.containers.list()
        print()
        print('docker containers:')
        for c in running_containers:
            print(c.name)
    except:
        print("docker section error")
    

    # get update db to match docker
    try:
        with app.app_context():
            scenarios_in_db = Scenarios.query.all()
            print()
            print("scenarios in db:")
            for s in scenarios_in_db:
                '''
                create set from active scenarios in both db and docker
                
                difference(*others)
                set - other - ...
                    Return a new set with elements in the set that are not in the others.
                '''
                print("type:",type(s))
                # s.name = s.name.replace("_", "")
                print(f"{s.name}\ttype: {s.description}\tstatus: {s.status}\tid: {s.id}")
    except:
        # send message to celery saying there are no scenarios
        print("no scenarios...?")

    # update db to match docker daemon state
    try:
        for c in running_containers:
            c_name = c.name.split('_')[0]
            print(c_name)
    except:
        pass
