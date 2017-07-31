"""Unit testing classes"""
from .api import create_app, db
import unittest


#test_func_edgecase
class TestAuthentication(unittest.TestCase):
    """this class contains tests for all user posible actions"""
    def setUP(self):
        """  """
        self.app = create_app('testing')
        # app.config.from_object('config.TestingConfig')
        test = self.app.test_client(self)

    def test_logout_success(self):
        ''' this method tests logout functionality'''
        test = self.app.test_client(self)
        response = test.get('/logout')
        assert(b'Logout success' in response.data)
       
    def test_login_incorrect_details(self):
        ''' tests that login doesnt work with wrong credentials'''
        test = self.app.test_client(self)
        response = test.post(
            '/login', data=dict(username="user12",
                                password="pass12"), follow_redirects=True)
        self.assertEqual(b'wrong username password combination', response.data)

    def test_login_successful(self):
        ''' tests that login doesnt work with wrong credentials'''
        test = self.app.test_client(self)
        response = test.post(
            '/login', data=dict(username="admin",
                                password="admin"), follow_redirects=True)
        self.assertEqual(b'login success', response.data)

    def test_add_user_empty_input(self):
        ''' test add user when input is empty - should return relevant message to user '''
        test = self.app.test_client(self)
        response = test.post(
            '/login', data=dict(username="",
            password="apsdsd"), follow_redirects=True)
        self.assertEqual(b'empty credentials', response.data)


if __name__ == '__main__':
    unittest.main()
