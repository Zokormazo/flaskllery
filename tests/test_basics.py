import unittest
import os
from flask import current_app
from app import app, db

class ModelsTestCase(unittest.TestCase):
	'''test models'''

	def setUp(self):
		app.config['TESTING'] = True
		app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////home/julen/projects/flaskllery/db/test.db'
		self.app = app.test_client()
		db.create_all()

	def tearDown(self):
		db.session.remove()
		db.drop_all()

	def test_app_exists(self):
		self.assertFalse(current_app is None)
if __name__ == '__main__':
    unittest.main()
