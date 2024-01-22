
# ---notes---
This document is to help track the progress of the migration from 
the legacy flask/jinja system to the new flask / react system 
using AJAX requests and responses.

Many of the functions will no longer need to be used, or will be 
done using other strategies.  The notes are in a free-form state 
at the moment, so plz bear with me. - Jonah (exoriparian)
# -----------

# These legacy Models may all find use w/ the new UI, in one form or another.  TBD.
# Each relates directly to a table in the db
from edurange_refactored.user.models import (
    User, 
    GroupUsers, 
    ScenarioGroups,
    Scenarios,
    StudentGroups,
    Responses,
    Notification
)

# the utils will mostly be replaced with a (sometimes very minorly) changed version
# new versions will mostly be in edurange_refactored.flask.modules.utils
from edurange_refactored.utils import (
    check_role_view, replaced by frontend validation and other role auth logic
    displayCorrectAnswers,  #DEV_TODO
    displayProgress,    #DEV_TODO
    flash_errors, deprecated and replaced by react updates
    getScore,   #DEV_TODO
    responseProcessing,  # replaced in modules.utils.scenario_utils
    getResponses, gets student's responses to specific question (legacy, not replaced)
    responseSelector, # ?????
    tempMaker, helper to prepare scenario content data
    queryPolish, # ?????
    questionReader, helper to forward json data
)

# forms will entirely be discontinued, and in some cases, replaced by schemas.  
# However, in many cases, these forms are only validating 1-2 items,
# meaning the requests can be validated within the routes themselves,
# and no schema (or form) will be necessary.
from edurange_refactored.user.forms import (
    RegisterForm,  replaced by RegisterSchema
    EmailForm,  no longer used
    changeEmailForm, replaced by UpdateEmailSchema
    GroupForm,  
    addUsersForm,
    manageInstructorForm,
    makeScenarioForm,
    modScenarioForm,
    scenarioResponseForm,
    deleteGroupForm,
    type1Form, # GroupForm, manageInstructorForm, deleteStudentForm
    type2Form, # addUsersForm, makeScenarioForm, modScenarioForm
    notifyDeleteForm,
)


Checklist
   
DONE
    User:
    - Login
    - Register
    - Change Email
    - Get Scenarios available to user (by x group)

    Instructor:
    - Create Scenario
    - Create User Group
    - Add Users to Group

    Scenario Guide:
    - Get Data for x scenario (readings & questions)
    - Evaluate x answer for y question
    - Get Unique Data (container IPs & ports) for x scenario
    - Get SSH Credentials (usernames & passwords) for x scenario, y user

    Other:

TODO (approx order of urgency):

    User:

    Instructor:
    - Start Scenario
    - Modify Senario
    - Stop Scenario
    - Delete Scenario
    - Get Bash History of User
    - Get Answers Data for User
    - Delete UserGroup
    - Delete User

    Scenario Guide:
    - displayCorrectAnswers
    - displayProgress replacement
    - User: Get my Answers to scenario Qs
    - User: Get a hint (algorithm dependent)

    



