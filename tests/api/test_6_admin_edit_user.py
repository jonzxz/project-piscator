import pytest
from test_2_authentication import login, register, logout
from app.models.User import User
from app import db
from app.utils.DBUtils import get_user_by_name

def test_edit_user(client, db):
    # Creates a new user to be disabled via direct database access
    TEST_DISABLE_USER = 'disableme'
    TEST_DISABLE_PASSWORD = 'password'

    new_user = User(username=TEST_DISABLE_USER)
    new_user.set_password(TEST_DISABLE_PASSWORD)
    db.session.add(new_user)
    db.session.commit()

    # Logs in to admin account via API and asserts successful log in
    USERNAME = 'admin'
    PASSWORD = 'password'
    login_response = login(client, USERNAME, PASSWORD)
    assert login_response.status_code == 200
    assert b'Administrator Dashboard' in login_response.data

    # Retrieves newly created user - gets ID, username and assert current status is ACTIVE
    user_to_disable = get_user_by_name(TEST_DISABLE_USER)
    user_to_disable_id = user_to_disable.get_id()
    user_to_disable_name = user_to_disable.get_username()
    # Assert user is active
    assert user_to_disable.get_active_status()

    # Sends POST request to disable user - sets is_active to None
    client.post(
    '/admin/user/edit/?id={}'.format(user_to_disable_id), data={
    'username' : '{}'.format(user_to_disable_name),
    # 'is_active' : True
    'is_active' : None
    },
    follow_redirects = True
    )

    # Assert user is now inactive
    assert get_user_by_name(TEST_DISABLE_USER).get_active_status() == False

    # Sends POST request to disable user - sets is_active to None
    client.post(
    '/admin/user/edit/?id={}'.format(user_to_disable_id), data={
    'username' : '{}'.format(user_to_disable_name),
    'is_active' : True
    },
    follow_redirects = True
    )

    # Assert user is now inactive
    assert get_user_by_name(TEST_DISABLE_USER).get_active_status() == True
