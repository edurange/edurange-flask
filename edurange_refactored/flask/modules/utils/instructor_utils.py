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



# - INSTRUCTOR: GENERATE USER GROUP W/ GROUP CODE
def createUserGroup():
    return 0


# - INSTRUCTOR: GENERATE GENERIC USER ACCTS FOR EXISTING GROUP
def generateTestAccts(acctCount):
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



