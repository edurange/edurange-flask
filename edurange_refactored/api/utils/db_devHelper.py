



from edurange_refactored.user.models import GroupUsers, ScenarioGroups, Scenarios, StudentGroups, User, Responses, Notification
from edurange_refactored.extensions import db


db_ses = db.session
    
skeleton_key_dict = {}

def get_user(input_name):

    user = User.query.filter_by(username=input_name).first()

    user_info = {
        "id": user.id,
        "username": user.username,
        "email": user.email,
        # "pwh": user.password.decode('utf-8'),  # this shouldn't be returned to the user
        "created_at": user.created_at,
        "active": user.active,
        "is_admin": user.is_admin,
        "is_instructor": user.is_instructor,
    }
    return user_info
def get_users():

    all_users = db_ses.query(User).all()
    all_users_list = []

    for user in all_users:
        user_info = {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            # "pwh": user.password.decode('utf-8'), # this shouldn't be returned to the user
            "created_at": user.created_at,
            "active": user.active,
            "is_admin": user.is_admin,
            "is_instructor": user.is_instructor,
        }
        all_users_list.append(user_info)
    return all_users_list

def get_groups():

    all_groups = db_ses.query(StudentGroups).all()
    all_groups_list = []

    for group in all_groups:
        group_info = {
            "id": group.id,
            "name": group.name,
            "owner_id": group.owner_id,
            "code": group.code,
            "hidden": group.hidden,
        }
        all_groups_list.append(group_info)
    return all_groups_list

def get_group_users():
    all_group_users = db_ses.query(GroupUsers).all()
    all_group_users_list = []

    for group_users in all_group_users:
        group_users_info = {
            "user_id": group_users.user_id,
            "group_id": group_users.group_id,
        }
        all_group_users_list.append(group_users_info)
    return all_group_users_list

def get_scenarios():

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
    return all_scenarios_list

def get_scenario_groups():

    all_scenario_groups = db_ses.query(ScenarioGroups).all()
    all_scenario_groups_list = []

    for scenario_group in all_scenario_groups:
        scenario_group_info = {
            "student_group_id": scenario_group.group_id,
            "scenario_group_id": scenario_group.scenario_id,
        }
        all_scenario_groups_list.append(scenario_group_info)
    return all_scenario_groups_list

def get_student_responses():

    all_student_responses = db_ses.query(Responses).all()
    all_student_responses_list = []
    for student_response in all_student_responses:
        student_response_info = {
            "response_id": student_response.group_id,
            "response_user_id": student_response.user_id,
            "response_scenario_id": student_response.scenario_id,
            "response_question": student_response.question,
            "response_content": student_response.content,
            "response_is_correct": student_response.correct,
            "response_time_stamp": student_response.response_time,
            "response_attempts_made": student_response.attempt,
        }
        all_student_responses_list.append(student_response_info)
    return all_student_responses_list

def get_instructor_data():

    instructor_all_info = [
    get_users(),
    get_groups(),
    get_group_users(),
    get_scenarios(),
    get_scenario_groups(),
    get_student_responses()          
    ]
    return instructor_all_info