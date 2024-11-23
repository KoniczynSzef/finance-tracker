from models.user import User


def test_user():
    user = User(username="test", email="test@test.com", full_name="Test User")

    assert user is not None
