users = []


def create_user(name, age):
    user = {
        "name": name,
        "age": age
    }

    users.append(user)
    return user


def get_users():
    return users