import json
import os
import yaml
import ast
from flask import abort

from edurange_refactored.extensions import db
from edurange_refactored.user.models import Scenarios, User, Responses

path_to_key = os.path.dirname(os.path.abspath(__file__))

## TESTED/WORKING

def getContent(scenario_id, username):
    db_ses = db.session
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

    unique_name = "".join(e for e in unique_name if e.isalnum())
    
    with open(f'data/tmp/{unique_name}/student_view/content.json', 'r') as fp:
        contentJSON = json.load(fp)
    with open(f'data/tmp/{unique_name}/students.json', 'r') as fp:
        credentialsJSON = json.load(fp)
    
    saniName = username.replace('-','')
    user_creds = credentialsJSON[saniName][0]
    if not user_creds: abort(418)
    return contentJSON, user_creds, unique_name

def getScenarioMeta(scenario_id):
        db_ses = db.session
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

def bashResponse(sid, uid, ans):
    db_ses = db.session

    uName = db_ses.query(User.username).filter(User.id == uid).first()[0]
    uName = "".join(e for e in uName if e.isalnum())

    sName = db_ses.query(Scenarios.name).filter(Scenarios.id == sid).first()[0]
    sName = "".join(e for e in sName if e.isalnum())

    if "${player.login}" in ans:
        students = open(f"./data/tmp/{sName}/students.json")
        user = ast.literal_eval(students.read())
        username = user[uName][0]["username"]
        ansFormat = ans[0:6]
        newAns = ansFormat + username
        return newAns
    elif "${scenario.instances" in ans:
        wordIndex = ans[21:-1].index(".")
        containerName = ans[21:21+wordIndex]
        containerFile = open(f"./data/tmp/{sName}/{containerName}.tf.json")
        content = ast.literal_eval(containerFile.read())
        index = content["resource"][0]["docker_container"][0][sName + "_" + containerName][0]["networks_advanced"]
        ans = ""
        for d in index:
            if d["name"] == (sName + "_PLAYER"):
                ans = d["ipv4_address"]

        return ans

    return ans

def readQuestions(scenario):
    scenario = "".join(e for e in scenario if e.isalnum())

    with open(f"./data/tmp/{scenario}/questions.yml") as yml:
        return yaml.full_load(yml)

def evaluateResponse(user_id, scenario_id, question_num, student_response):
    """Check student answer matches correct one from YAML file."""
    db_ses = db.session
    scenario = db_ses.query (Scenarios).filter_by(id=scenario_id).first()
    scenario_uniqueName = scenario.name
    questions = readQuestions(scenario_uniqueName)
    question = questions[question_num-1]

    responseData = []

    print("evaluateResponse says student_response: ", student_response)

    for i in question['Answers']:

        correctResponse = str(i['Value'])

        tempResponseItem = {
            "submitted_response":student_response,
            "correct_response":correctResponse,
            "points_awarded":0
        }

        if "${" in correctResponse:
            correctResponse = bashResponse(scenario_id, user_id, correctResponse)

        if student_response == correctResponse or correctResponse == 'ESSAY':
            pointsAwarded = i['Points']
            tempResponseItem['points_awarded'] = pointsAwarded

        responseData.append (tempResponseItem)
    return responseData

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
