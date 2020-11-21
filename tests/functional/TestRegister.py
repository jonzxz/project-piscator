from app import app

import unittest

# Test with
# nose2 -v app.tests.TestRegister
class TestRegister(unittest.TestCase):
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

    def register(self, username, password, confirm_password):
        return self.app.post(
        '/register', data={
        'username' : username,
        'password' : password,
        'confirm_password' : confirm_password
        },
        follow_redirects=True
        )

    ## Make sure user does not exist in database!!
    def test_valid_register(self):
        response = self.register('user10', 'password10', 'password10')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'dashboard', response.data)

    def Atest_invalid_register(self):
        response = self.register('user6', 'password6', 'PASSWORD6')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'dashboard', response.data)

if __name__ == "__main__":
    unittest.main()
    # suite = unittest.TestSuite()
    # suite.addTest(Test('test1'))
    # unittest.TextTestRunner().run(suite)
