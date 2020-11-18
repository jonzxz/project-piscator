from app import app
from flask_login import current_user, login_user

import unittest

# Test with
# nose2 -v app.tests.TestLogin
class TestLogin(unittest.TestCase):
    @classmethod
    def setupClass(cls):
        pass

    @classmethod
    def tearDownClass(cls):
        pass

    def setUp(self):
        # If these two are not set, PasswordField will not work because of invalid CSRF Tokens
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        self.app = app.test_client()
        self.app.testing = True

    def tearDown(self):
        pass

    def test_home_status_code(self):
        result = self.app.get('/')
        self.assertEqual(result.status_code, 200)

    def login(self, username, password):
        return self.app.post(
        '/login', data={
        'username' : username,
        'password' : password
        },
        follow_redirects=True
        )

    def test_valid_login(self):
        response = self.login('user1', 'password')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'dashboard', response.data)

    def Atest_invalid_login(self):
        response = self.login('qweqwe', '123456')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'dashboard', response.data)

if __name__ == "__main__":
    unittest.main()
    # suite = unittest.TestSuite()
    # suite.addTest(Test('test1'))
    # unittest.TextTestRunner().run(suite)
