


"""Helper utilities and decorators."""
import json
import os

import yaml
import markdown as md
import ast
from flask import abort, flash, request, url_for, jsonify
from flask_login import current_user
from markupsafe import Markup


from edurange_refactored.extensions import db
db_ses = db.session

from edurange_refactored.user.models import Scenarios, User, Responses

path_to_key = os.path.dirname(os.path.abspath(__file__))

## TESTED/WORKING

def getContent(scenario_id, username):
    # db_ses = db.session
    statusSwitch = {
        0: "Stopped",
        1: "Started",
        2: "Something went very wrong",
        3: "Starting",
        4: "Stopping",
        5: "ERROR",
        7: "Building"
    }
    status = db_ses.query(Scenarios.status).filter(Scenarios.id == scenario_id).first()
    status = statusSwitch[status[0]]

    unique_name = db_ses.query(Scenarios.name).filter(Scenarios.id == scenario_id).first()
    if unique_name: unique_name = unique_name[0]
    if (not unique_name
    or status != "Started"): abort(418) 
    
    with open(f'data/tmp/{unique_name}/student_view/content.json', 'r') as fp:
        contentJSON = json.load(fp)
    with open(f'data/tmp/{unique_name}/students.json', 'r') as fp:
        credentialsJSON = json.load(fp)
    
    saniName = username.replace('-','')
    user_creds = credentialsJSON[saniName][0]
    if not user_creds: abort(418)
    return contentJSON, user_creds, unique_name

def getScenarioMeta(scenario_id):
        
        scenario = db_ses.query (Scenarios).filter_by(id=scenario_id).first()

        scenario_info = {
            "scenario_id": scenario.id,
            "scenario_name": scenario.name,
            "scenario_description": scenario.description,
            "scenario_owner_id": scenario.owner_id,
            "scenario_created_at": scenario.created_at,
            "scenario_status": scenario.status,
        }
        return scenario_info



### UNTESTED / DEV 
    
# def getResponses(req_user_id, req_attempt, req_query, req_questions):
#     responses = []
#     entries = [
#         entry 
#         for entry 
#         in req_query 
#         if entry.user_id == req_user_id 
#         # and entry.attempt == req_attempt
#     ]

#     for response in entries:
#         question_number = response.question_data
#         question_data = req_questions[question_number-1]

#         responses.append({
#             'number': question_number,
#             'question': question_data['Text'],
#             'answer': question_data['Answers'][0]['Value'],
#             'points': question_data['Points'],
#             'student_response': response.student_response,
#             'earned': response.points
#         })

#     return responses
    

    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    ################## notes / scratch #################
    
    
    # # the db property of `.description` (assigned to scenario_title variable here) 
    # # is the generic name for a scenario, e.g. 'Getting_Started'
    # scenario_title = db_ses.query(Scenarios.description).filter(Scenarios.id == scenario_id).first()
    # scenario_title = scenario_title[0]

    # # getDescription returns the short description, or 'blurb', for a scenario
    # # e.g. "This game uses strace to examine executable files."
    # # pulls values from "./scenarios/prod/{scenario}/{scenario}.yml"
    # # '{scenario}' here is the title in lower_snake, e.g. 'getting_started'
    # # blurb = getDescription(scenario_title)

    
    # # guide = None #getGuide(scenario_title)
    
    
    # # questions = getQuestions(scenario_title)

    # # sName = db_ses.query(Scenarios.name).filter(Scenarios.id == scenario_id).first()
    # # sName = sName[0]

    # # if user_role == "ins":
    # #     createdAt = db_ses.query(Scenarios.created_at).filter(Scenarios.id == scenario_id).first()
    # #     createdAt = createdAt[0]

    # #     return status, ownerName, createdAt, blurb, scenario_title, sName, guide, questions
    # # elif user_role == "stu":
    # #     username = db_ses.query(User.username).filter(User.id == user_id).first()[0]
    # #     username = "".join(e for e in username if e.isalnum())
    # #     pw = getPass(sName, username)

    # #     return status, ownerName, blurb, scenario_title, sName, username, pw, guide, questions
