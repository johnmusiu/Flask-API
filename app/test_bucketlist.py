"""Unit testing classes"""
from .api import create_app, db
import unittest
import json

class TestBucketlist(unittest.TestCase):
    """this class contains tests for all user posible actions"""
    def setUp(self):
        """ setup the testing parameters(configuration)
    	 setup values to be reused in other tests """
        self.app = create_app('testing')
        self.client = self.app.test_client
        self.bucketlist = {'title': 'Go to the zoo'}

        #bind app to the current context
        with self.app.app_context():
            #create tables (as defined in model)
            db.create_all()

    def test_add_bl_success(self):
        ''' check if bucketlist is added successfully '''
        result = self.client().post('/bucketlists/', data=self.bucketlist)
        self.assertEqual(result.status_code, 200)
        self.assertIn('Go to the zoo', str(result.data))

    def test_view_bl_success(self):
        res = self.client().post('/bucketlists/1', data = {'title': 'For crying out loud'})
        self.assertEqual(res.status_code, 201)
        result = self.client().get('/bucketlists/')
        self.assertEqual(result.status, 200)
        self.assertIn('Go to the zoo', str(result.data))

    def test_bucketlists_get_by_id(self):
        rev = self.client().post('/bucketlists/', data=self.bucketlist)
        self.assertEqual(rev.status_code, 201)
        result_in_json = json.loads(rev.data.decode('utf-8').replace("'", "\""))
        result = self.client().get('/bucketlists/{}'.format(result_in_json['id']))
        self.assertEqual(result.status_code, 200)
        self.assertIn('Go to the zoo', str(result.data))

    def test_bl_edit_success(self):
        ''' tests update bucketlist works '''
        rv = self.client().post('/bucketlists/', data=self.bucketlist)
        self.assertEqual(rv.status_code, 201)
        rv = self.client().put('/bucketlists/1', data={'title': 'For everyone\'s sake'})
        self.assertEqual(rv.status_code, 200)
        results = self.client().get('/bucketlists/1')
        self.assertIn('For everyone\'s sake', str(results.data))

    def test_delete_bl_success(self):
        ''' tests tht the app doesnt break if bl id passed to delete func not found '''
        rv = self.client().put('/bucketlists/1', data={'title': 'For crying out loud'})
        self.assertEqual(rv.status_code, 201)
        res = self.client().delete('/bucketlists/1')
        self.assertEqual(res.status_code, 200)
        #check if delete worked, return 404 if it did delete item
        result = self.client().get('/bucketlists/1')
        self.assertEqual(result.status_code, 404)

    #test for error 401: restricted view (when not logged in)
    
    def tearDown(self):
        """ do away with all initialized variables """
        with self.app.app_context():
            #delete all tables (drop)
            db.session.remove()
            db.drop_all
    
if __name__ == '__main__':
    unittest.main()
