# -*- coding: utf-8 -*-
"""The app module, containing the app factory function."""
import logging
import sys
import os
import signal
from time import sleep

from celery import Celery
from flask import Flask, render_template
from sqlalchemy.orm import with_expression

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
from edurange_refactored.settings import CELERY_BROKER_URL
from edurange_refactored.user.models import User, Scenarios
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


def sync_docker(app):
    import docker
    from edurange_refactored.user.models import Scenarios
    """Synchronize the state of the Docker daemon 
    with the database/what Flask shows on the scenarios page"""

    # get state of db
    try:
        with app.app_context():
            scenarios_in_db = Scenarios.query.all()
            print("scenarios:")
            for s in scenarios_in_db:
                print("\t", s.name)
    except:
        # send message to celery saying there are no scenarios
        print("no scenarios...?")

    # compare against state of docker
    print()
    try:
        client = docker.from_env()
        active_containers = client.containers.list()
        print(active_containers)

        # match names of scenarios_in_db to active containers from docker client

        print("docker section no error")
    except:
        print("docker section error")

    # make changes to
