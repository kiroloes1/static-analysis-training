from src.user_service import create_user, get_users


def test_create_user():
    user = create_user("Ahmed", 20)

    assert user["name"] == "Ahmed"
    assert user["age"] == 20


def test_get_users():
    assert isinstance(get_users(), list)