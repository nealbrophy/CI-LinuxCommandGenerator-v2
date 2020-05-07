from app import app
import unittest

class FlaskTest(unittest.TestCase):

    def test_index(self):
        tester = app.test_client(self)
        response = tester.get('/', content_type='html/text')
        self.assertEqual(response.status_code, 200)
    
    def test_distros(self):
        tester = app.test_client(self)
        response = tester.get('/', content_type='html/text')
        self.assertTrue(b'List of Distros & Commands' in response.data)
        self.assertTrue(b'Ubuntu' in response.data)






if __name__ == '__main__':
    unittest.main()
