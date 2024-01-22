import json
import os
import yaml
import ast
import docker
from flask import abort
import string
import random
from ..utils.account_utils import register_user

from edurange_refactored.extensions import db
from edurange_refactored.user.models import Scenarios, User, Responses

path_to_key = os.path.dirname(os.path.abspath(__file__))

## whole file is currently WIP 1/17/24 -Jonah (exoriparian)

def generate_registration_code(size=8, chars=string.ascii_lowercase + string.digits):
    return "".join(random.choice(chars) for _ in range(size))

# - INSTRUCTOR: GENERATE USER GROUP W/ GROUP CODE
def createUserGroup():
    return 0


# - INSTRUCTOR: GENERATE GENERIC USER ACCTS FOR EXISTING GROUP
def generateTestAccts(new_user_count, group_name, group_code):

    # check for code input
    if not group_code:
        print('You must have group code')
    # check to see if code is in database
        # if code NOT in database, reject request

    generatedUsers = []
    for i in range(new_user_count):

        newPass = generate_registration_code()
        user_obj = {
            'username' : group_name + '-' + i,
            'password' : newPass,
            'confirm_password' : newPass,
            'code' : group_code,
            'email': 'DEV_ONLY@EMAIL.COM'
        }

        register_user(user_obj)

    return []


# - INSTRUCTOR: CREATE/START/STOP/DESTROY SCENARIOS
def createScenario(scenario_unique_name, scenario_generic_name):
    return 0

def populateScenario(scenario_unique_name, scenario_generic_name):
    # this process should look through the current list of users
    # and their group association, and then create the user accts
    # for the scenario.  if the user association is already good
    # to go, we can skip that user, OR we can just create a new
    # set of user data (including re-making existing user info).  
    # not sure which is better at the moment...
    return 0
def startScenario(scenario_id):
    return 0
def stopScenario(scenario_id):
    return 0
def destroyScenario(scenario_id):
    # clean up everything so no hanging chads
    return 0

# - ASSIGN USERS/GROUPS TO SCENARIO
def assignUserToGroup(user_id, group_id):
    return 0
def removeUserFromGroup(user_id, group_id):
    return 0

    #   - CREATE USER INFO FOR SCENARIO (ALLOW FOR UPDATING IN CASE STUDENT ACCT CREATED AFTER SCENARIO)



