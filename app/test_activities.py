"""Unit testing classes"""
import json
import unittest
from .api import create_app, db

#test_func_edgecase
class TestActivities(unittest.TestCase):
    """this class contains tests for all user posible actions"""
    def setUP(self):
        """ setup the testing parameters(configuration)
    	 setup values to be reused in other tests """
        self.app = create_app('development')
        self.client = self.app.test_client
        self.item = {'title': 'Take snap with simba'}

        #bind app to the current context
        with self.app.app_context():
            #create tables (as defined in model)
            db.create_all()

    def test_items_put_success(self):
        ''' check if item is added successfully '''
        result = self.client().post('/bucketlists/1/items/', data=self.item)
        self.assertEqual(result.status_code, 200)
        self.assertIn('Take snap with simba', str(result.data))

    def test_items_view_success(self):
        res = self.client().put('/bucketlists/1/items/', data = {'title': 'Maasai mara'})
        self.assertEqual(res.status_code, 201)
        result = self.client().get('/bucketlists/1/items/')
        self.assertEqual(result.status, 200)
        self.assertIn('Maasai mara', str(result.data))

    def test_bl_edit_success(self):
        ''' tests update items works '''
        rv = self.client().post('/bucketlists/1/items/', data=self.item)
        self.assertEqual(rv.status_code, 201)
        rv = self.client().put('/bucketlists/1/items/1', data={'title': 'Tsavo'})
        self.assertEqual(rv.status_code, 200)
        results = self.client().get('/bucketlists/1/items/1')
        self.assertIn('Tsavo', str(results.data))

    def test_delete_task_success(self):
        ''' tests tht the delete item works '''
        rv = self.client().put('/bucketlists/1/items/', data={'title': 'Tsavo'})
        self.assertEqual(rv.status_code, 201)
        res = self.client().delete('/bucketlists/1/items/1')
        self.assertEqual(res.status_code, 200)
        #check if delete worked, return 404 if it did delete item
        result = self.client().get('/bucketlists/1/items/')
        self.assertEqual(result.status_code, 404)

    def tearDown(self):
        """ do away with all initialized variables """
        with self.app.app_context():
            #delete all tables (drop)
            db.session.remove()
            db.drop_all
    
if __name__ == '__main__':
    unittest.main()
