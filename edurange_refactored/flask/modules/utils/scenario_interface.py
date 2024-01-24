
from edurange_refactored.extensions import db
# from common_utils import g
from edurange_refactored.user.models import User, GroupUsers, StudentGroups, Scenarios
from edurange_refactored.notification_utils import NotifyCapture
from edurange_refactored.tasks import CreateScenarioTask
from edurange_refactored.scenario_utils import gen_chat_names
from flask import jsonify, g

def scenario_create(scenario_type, scenario_name, scen_group_name):
    db_ses = db.session
    owner_user_id = g.current_user_id

    students = (
        db_ses.query(User.username)
        .filter(StudentGroups.name == scen_group_name)
        .filter(StudentGroups.id == GroupUsers.group_id)
        .filter(GroupUsers.user_id == User.id)
        .all()
    )

    Scenarios.create(name=scenario_name, description=scenario_type, owner_id=owner_user_id)
    NotifyCapture(f"Scenario {scenario_name} has been created.")
    
    scenario_id = db_ses.query(Scenarios.id).filter(Scenarios.name == scenario_name).first()
    # scenario_id_list = list(scenario_id._asdict().values())[0]
    scenario_id = scenario_id._asdict()
    print('PRINTING SCENARIO_ID: ',scenario_id)
    scenario_id = scenario_id['id']
    scenario = Scenarios.query.filter_by(id=scenario_id).first()
    scenario.update(status=7)
    group_id = db_ses.query(StudentGroups.id).filter(StudentGroups.name == scen_group_name).first()
    group_id = group_id._asdict()

    # Convert the students list to a list of dictionaries
    students_list = [{'username': student['username']} for student in students]

    group_id = group_id["id"]
    student_ids = db_ses.query(GroupUsers.id).filter(GroupUsers.group_id == group_id).all()

    namedict = gen_chat_names(student_ids, scenario_id)

    group_name = 'goob'
        # 
    #            args: self, scenario_name, scenario_type, owner_user_id, group_name,    group_id, scenario_id,      namedict
    CreateScenarioTask.delay(scenario_name, scenario_type, owner_user_id, group_name,    group_id, scenario_id,      namedict)

    # Return the list of students as a JSON response
    return jsonify({"student_list": students_list})

# def scenario_create(scenario_type, scenario_name, scen_group_name):

#     db_ses = db.session
#     owner_user_id = g.current_user_id

#     students = (
#         db_ses.query(User.username)
#         .filter(StudentGroups.name == scen_group_name)
#         .filter(StudentGroups.id == GroupUsers.group_id)
#         .filter(GroupUsers.user_id == User.id)
#         .all()
#     )

#     Scenarios.create(name=scenario_name, description=scenario_type, owner_id=owner_user_id)
#     NotifyCapture(f"Scenario {scenario_name} has been created.")
    
#     scenario_id = db_ses.query(Scenarios.id).filter(Scenarios.name == scenario_name).first()
#     scenario_id_list = list(scenario_id._asdict().values())[0]

#     scenario = Scenarios.query.filter_by(id=scenario_id_list).first()
#     scenario.update(status=7)
#     group_id = db_ses.query(StudentGroups.id).filter(StudentGroups.name == scen_group_name).first()
#     group_id = group_id._asdict()

    
#     for i, student in enumerate(students):
#         students[i] = student._asdict()

#     # scenario_id, group_id = scenario_id._asdict(), group_id._asdict()

#     group_id = group_id["id"]
#     student_ids = db_ses.query(GroupUsers.id).filter(GroupUsers.group_id == group_id).all()

#     namedict = gen_chat_names(student_ids, scenario_id_list)

#     CreateScenarioTask.delay(scenario_name, scenario_type, owner_user_id, students, group_id, scenario_id_list, namedict)

#     return jsonify ({"student_list": students})

def list_all_scenarios(requestJSON):
    print("Performing LIST method")
    
    db_ses = db.session

    all_scenarios = db_ses.query(Scenarios).all()
    all_scenarios_list = []
    for scenario in all_scenarios:
        scenario_info = {
            "scenario_id": scenario.id,
            "scenario_name": scenario.name,
            "scenario_description": scenario.description,
            "scenario_owner_id": scenario.owner_id,
            "scenario_created_at": scenario.created_at,
            "scenario_status": scenario.status,
        }
        all_scenarios_list.append(scenario_info)
    return jsonify({"scenarios_list":all_scenarios_list})