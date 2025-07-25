import unittest
from app import app

class FlaskTestCase(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()

    def test_hello(self):
        response = self.app.get('/api/hello')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {'hello': 'world'})

    def test_hello_name(self):
        response = self.app.get('/api/hello/ben')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {'hello': 'ben'})

if __name__ == '__main__':
    unittest.main()