import os 
from os import path
if path.exists("env.py"):
  import env 
from flask_pymongo import PyMongo
from app import app
import unittest
import random
from form import csrf

app.config["MONGO_DBNAME"] = 'linuxCmdGen'
app.config["MONGO_URI"] = os.environ.get('MONGO_URI')
app.config["SECRET_KEY"] = os.environ.get('SECRET_KEY')
csrf.init_app(app)
mongo = PyMongo(app)
distros = mongo.db.distros.find()

class FlaskTest(unittest.TestCase):

    def test_home(self):
        tester = app.test_client(self)
        response = tester.get('/', content_type='html/text')
        self.assertEqual(response.status_code, 200)
    
    def test_distro_view(self):
        tester = app.test_client(self)
        response = tester.get('/', content_type='html/text')
        for distro in distros:
            name = distro['distro_name']
            self.assertTrue(b'name' in response.data)
    
    def test_find(self):
        tester = app.test_client(self)
        response = tester.post(
            '/find_command', 
            data=dict(app_name='chrome', app_distro='Ubuntu'),
            follow_redirects=True,
            csrf=csrf
            )
        self.assertIn(b'sudo', response.data)
        
        







if __name__ == '__main__':
    unittest.main()
