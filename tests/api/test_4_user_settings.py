from test_2_authentication import login
from app.models.User import User
import pytest
from app.utils.DBUtils import get_user_by_name

def change_user_settings_password(client, username, current_password, new_password, conf_new_password):
    return client.post(
    '/dashboard/account/update_password', data={
    'username' : username,
    'current_password' : current_password,
    'new_password' : new_password,
    'confirm_new_password' : conf_new_password
    },
    follow_redirects=True
    )

def change_user_settings_disable_acc(client, username, current_password, disable_account):
    return client.post(
    '/dashboard/account/disable', data={
    'username' : username,
    'current_password' : current_password,
    'disable_account' : disable_account
    },
    follow_redirects=False
    )

def enable_account(client, db):
    USERNAME = 'testuser123'
    user = get_user_by_name(USERNAME)
    user.set_active_status(True)
    db.session.commit()

def test_invalid_change_no_password(client, db):
    USERNAME = 'testuser123'
    CURRENT_PW = 'password'
    login(client, USERNAME, CURRENT_PW)
    change_user_settings_password(client, USERNAME, '', '', '')
    user = get_user_by_name(USERNAME)
    assert not (user.check_password(''))

def test_invalid_change_wrong_current_password(client, db):
    USERNAME = 'testuser123'
    CURRENT_PW = 'password'
    WRONG_CURRENT_PW = 'password123'
    NEW_PW = 'newpassword'
    CONF_NEW_PW = 'newpassword'
    login(client, USERNAME, CURRENT_PW)
    change_user_settings_password(client, USERNAME, WRONG_CURRENT_PW, NEW_PW, CONF_NEW_PW)
    user = get_user_by_name(USERNAME)
    assert not (user.check_password(NEW_PW))

def test_invalid_change_mismatched_password(client, db):
    USERNAME = 'testuser123'
    CURRENT_PW = 'password'
    NEW_PW = 'newpassword'
    CONF_NEW_PW = 'newpassword123'
    login(client, USERNAME, CURRENT_PW)
    change_user_settings_password(client, USERNAME, CURRENT_PW, NEW_PW, CONF_NEW_PW)
    user = get_user_by_name(USERNAME)
    assert not (user.check_password(NEW_PW))

def test_valid_change_password(client, db):
    USERNAME = 'testuser123'
    CURRENT_PW = 'password'
    NEW_PW = 'newpassword'
    CONF_NEW_PW = 'newpassword'
    login(client, USERNAME, CURRENT_PW)
    change_user_settings_password(client, USERNAME, CURRENT_PW, NEW_PW, CONF_NEW_PW)
    assert get_user_by_name(USERNAME).check_password(NEW_PW)

def test_disable_account_without_slider(client, db):
    USERNAME = 'testuser123'
    CURRENT_PW = 'newpassword'
    DISABLE_ACCOUNT = "off"
    login(client, USERNAME, CURRENT_PW)
    change_user_settings_disable_acc(client, USERNAME, CURRENT_PW, DISABLE_ACCOUNT)
    user = get_user_by_name(USERNAME)
    assert user.get_active_status()

def test_disable_account_without_password(client, db):
    USERNAME = 'testuser123'
    CURRENT_PW = 'newpassword'
    EMPTY_CURRENT_PW = ''
    DISABLE_ACCOUNT = "on"
    login(client, USERNAME, CURRENT_PW)
    change_user_settings_disable_acc(client, USERNAME, EMPTY_CURRENT_PW, DISABLE_ACCOUNT)
    user = get_user_by_name(USERNAME)
    assert user.get_active_status()

def test_disable_account_wrong_password(client, db):
    USERNAME = 'testuser123'
    CURRENT_PW = 'newpassword'
    DISABLE_ACCOUNT = "on"
    WRONG_CURRENT_PW = 'password'
    login(client, USERNAME, CURRENT_PW)
    change_user_settings_disable_acc(client, USERNAME, WRONG_CURRENT_PW, DISABLE_ACCOUNT)
    user = get_user_by_name(USERNAME)
    assert user.get_active_status()

def test_disable_account_with_passwords(client, db):
    USERNAME = 'testuser123'
    CURRENT_PW = 'newpassword'
    DISABLE_ACCOUNT = "on"
    login(client, USERNAME, CURRENT_PW)
    change_user_settings_disable_acc(client, USERNAME, CURRENT_PW, DISABLE_ACCOUNT)
    user = get_user_by_name(USERNAME)
    assert not user.get_active_status()
