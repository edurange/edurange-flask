# -*- coding: utf-8 -*-
"""Tutorials views."""
from flask import (
    Blueprint,
    render_template
)

from ..scenario_utils import (
    populate_catalog
)

from edurange_refactored.extensions import db
from edurange_refactored.user.models import Scenarios

blueprint = Blueprint(
    "tutorials", __name__, url_prefix="/tutorials", static_folder="../static"
)


@blueprint.route("/")
def list():
    """List of scenarios"""
    #
    scenarios = populate_catalog()
    return render_template("tutorials/list.html", scenarios=scenarios)


@blueprint.route("/File_Wrangler")
def fw():
    """File Wrangler Codelab"""
    return render_template("tutorials/File_Wrangler/index.html")


@blueprint.route("/Getting_Started")
def gs():
    """Getting Started Codelab"""
    return render_template("tutorials/Getting_Started/index.html")


@blueprint.route("/Ssh_Inception")
def si():
    """Ssh Inception Codelab"""
    return render_template("tutorials/Ssh_Inception/index.html")


@blueprint.route("/Total_Recon")
def tr():
    """Total Recon Codelab"""
    return render_template("tutorials/Total_Recon/index.html")

