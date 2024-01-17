
from edurange_refactored.user.models import GroupUsers, StudentGroups, User

# account utils available to student (e.g. non-instructor) routes

# create student account (add to postgreSQL db)
def register_user(validated_registration_data):
    data = validated_registration_data
    User.create(
            username=data["username"],
            email=data["email"],
            password=data["password"],
            active=True,
    )
       
    group = StudentGroups.query.filter_by(code=data["code"]).first()
    user = User.query.filter_by(username=data["username"]).first()
    group_id = group.get_id()
    user_id = user.get_id()
    GroupUsers.create(user_id=user_id, group_id=group_id)

# update email
    
# delete account