from test_2_authentication import login
from app.models.User import User
import pytest
from app.utils.DBUtils import get_user_by_name

def change_user_settings(client, username, current_password, new_password, conf_new_password, disable_account):
    return client.post(
    '/dashboard/account', data={
    'username' : username,
    'current_password' : current_password,
    'new_password' : new_password,
    'confirm_new_password' : conf_new_password,
    'disable_account' : disable_account
    },
    follow_redirects=False
    )

def enable_account(client, db):
    USERNAME = 'testuser123'
    user = get_user_by_name(USERNAME)
    user.update_active_status(True)
    db.session.commit()

def test_valid_change_password(client, db):
    USERNAME = 'testuser123'
    CURRENT_PW = 'password'
    NEW_PW = 'newpassword'
    CONF_NEW_PW = 'newpassword'
    DISABLE_ACCOUNT = None
    login(client, USERNAME, CURRENT_PW)
    change_user_settings(client, USERNAME, CURRENT_PW, NEW_PW, CONF_NEW_PW, DISABLE_ACCOUNT)
    user = get_user_by_name(USERNAME)
    assert (user.check_password(NEW_PW))

def test_invalid_change_mismatched_password(client, db):
    USERNAME = 'testuser123'
    CURRENT_PW = 'newpassword'
    NEW_PW = 'evenwrongerpassword'
    CONF_NEW_PW = 'superultrawrongpassword'
    DISABLE_ACCOUNT = None
    login(client, USERNAME, CURRENT_PW)
    change_user_settings(client, USERNAME, CURRENT_PW, NEW_PW, CONF_NEW_PW, DISABLE_ACCOUNT)
    user = get_user_by_name(USERNAME)
    assert not (user.check_password(NEW_PW))

def test_invalid_change_wrong_current_password(client, db):
    USERNAME = 'testuser123'
    CURRENT_PW = 'wrongpassword'
    NEW_PW = 'strongpassword'
    CONF_NEW_PW = 'strongpassword'
    DISABLE_ACCOUNT = None
    login(client, USERNAME, CURRENT_PW)
    change_user_settings(client, USERNAME, CURRENT_PW, NEW_PW, CONF_NEW_PW, DISABLE_ACCOUNT)
    user = get_user_by_name(USERNAME)
    assert not (user.check_password(NEW_PW))

def test_disable_account_only(client, db):
    USERNAME = 'testuser123'
    CURRENT_PW = 'newpassword'
    NEW_PW = None
    CONF_NEW_PW = None
    DISABLE_ACCOUNT = "on"
    login(client, USERNAME, CURRENT_PW)
    change_user_settings(client, USERNAME, CURRENT_PW, NEW_PW, CONF_NEW_PW, DISABLE_ACCOUNT)
    user = get_user_by_name(USERNAME)
    assert not user.get_active_status()
    enable_account(client, db)

def test_disable_account_with_passwords(client, db):
    USERNAME = 'testuser123'
    CURRENT_PW = 'newpassword'
    NEW_PW = "newerpassword"
    CONF_NEW_PW = "newerpassword"
    DISABLE_ACCOUNT = "on"
    login(client, USERNAME, CURRENT_PW)
    change_user_settings(client, USERNAME, CURRENT_PW, NEW_PW, CONF_NEW_PW, DISABLE_ACCOUNT)
    user = get_user_by_name(USERNAME)
    assert not user.check_password(NEW_PW)
    assert not user.get_active_status()
