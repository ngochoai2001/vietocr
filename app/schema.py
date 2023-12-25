from model.auth import User


def user_serializer(user) -> dict:
    return {
        'id' : str(user["_id"]),
        'full_name': user["full_name"],
        'user_name': user["user_name"],
        'pass_word': user["pass_word"],
    
    }

def users_serializer(users) -> list:
    return [user_serializer(user) for user in users ]
