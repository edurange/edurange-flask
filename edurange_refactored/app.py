# -*- coding: utf-8 -*-
"""The app module, containing the app factory function."""
import logging
import sys
from datetime import datetime

from flask import Flask, render_template
from flask_login import current_user
from flask_socketio import SocketIO

from edurange_refactored.public_sister.views_sister import blueprint_routing_sister
from edurange_refactored import commands, public, user, tutorials, api
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
from edurange_refactored.user.models import User

socketapp = SocketIO()


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
    register_jinja_filters(app)
    socketapp.init_app(app)

    return app


def register_jinja_filters(app):
    app.jinja_env.filters["formatdatetime"] = format_datetime
    app.jinja_env.filters["ctime"] = timectime
    app.jinja_env.globals.update(Aid=Aid)
    app.jinja_env.globals.update(Iid=Iid)
    app.jinja_env.globals.update(get_role=get_role)

def register_extensions(app):
    """Register Flask extensions."""
    bcrypt.init_app(app)
    cache.init_app(app)
    db.init_app(app)

#####
    csrf_protect.init_app(app) # THIS APPWIDE CSRF DISABLED FOR DEV -> IMPLEMENTED ELSEWHERE IN ROUTES - WILL NEED TO FIX
#####

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
    app.register_blueprint(blueprint_routing_sister)
    app.register_blueprint(api.contents.blueprint)

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


def format_datetime(value, format="%d %b %Y %I:%M %p"):
    """Format a date time to (Default): d Mon YYYY HH:MM P"""
    if value is None:
        return ""

    return value.strftime(format)


def timectime(s):
    return datetime.fromtimestamp(int(s))


def Aid():
    user = User.query.filter_by(id=current_user.id).first()

    return user.is_admin


def Iid():
    user = User.query.filter_by(id=current_user.id).first()

    return user.is_instructor


def get_role():
    if current_user and current_user.is_authenticated:
        user = User.query.filter_by(id=current_user.id).first()

        if user.is_admin and user.is_instructor:
            return "a/i"  # this option may not be needed
        elif user.is_admin:
            return "a"
        elif user.is_instructor:
            return "i"
        else:
            return "s"

    return None  # no role --> not logged in
