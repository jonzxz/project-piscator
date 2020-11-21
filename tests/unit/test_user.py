from app.models.User import User

def test_new_user():
    user = User(username='testuser123')
    user.set_password('password1')
    assert user.get_username() == 'testuser123'
    assert not user.password == 'password1'
    assert user.get_admin_status() == False
