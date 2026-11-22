users = []


def create_user(name, age):
    user = {
        "name": name,
        "age": age,
        "is_active": True
    }

    users.append(user)
    return user


def get_users():
    return users

def delete_user(name):
    global users

    users = [user for user in users if user["name"] != name]