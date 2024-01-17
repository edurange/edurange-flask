import json
import os
import yaml
import ast
import docker
from flask import abort

from edurange_refactored.extensions import db
from edurange_refactored.user.models import Scenarios, User, Responses

path_to_key = os.path.dirname(os.path.abspath(__file__))

## whole file is currently WIP 1/17/24 -Jonah (exoriparian)

# - CHANGE USER ROLE
# - CHANGE USER INFO DIRECTLY (LIKE EMAIL)

