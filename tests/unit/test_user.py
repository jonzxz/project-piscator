from datetime import datetime

# Test username is set correctly
def test_user_username(user):
    assert user.get_username() == 'testuser123'

# Test password is set correctly
def test_user_password_hash(user):
    assert user.check_password('password1')

# Test password is hashed
def test_user_password(user):
    assert not user.password == 'password1'

# Test user active status changes
def test_user_active_status(user):
    # Assert user is active
    user.set_active_status(True)
    assert user.get_active_status()

    # Assert user is disabled
    user.set_active_status(False)
    assert not user.get_active_status()

# Test user admin status changes
def test_user_admin_status(user):
    # Assert user is not admin
    user.set_admin_status(False)
    assert not user.get_admin_status()

    # Assert user is promoted to admin
    user.set_admin_status(True)
    assert user.get_admin_status()

# Test user last logged in
def test_user_last_logged_in(user):
    # Assert last logged in is None
    assert not user.get_last_logged_in()

    time = datetime.now()
    user.set_last_logged_in(time)
    assert user.get_last_logged_in() == time

def test_user_reset_token(user):
    # Assert reset token is none by default
    assert not user.get_reset_token()

    # Assert reset token is generated
    user.generate_reset_token()
    assert user.get_reset_token()

    # Assert reset token is purged
    user.delete_reset_token()
    assert not user.get_reset_token()
