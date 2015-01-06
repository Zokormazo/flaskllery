import unittest
import os
from flask import current_app
from app import create_app, db

class ModelsTestCase(unittest.TestCase):
	'''test models'''

	def setUp(self):
		self.app = create_app('testing')
		db.create_all()

	def tearDown(self):
		db.session.remove()
		db.drop_all()

	def test_app_exists(self):
		self.assertFalse(current_app is None)

	def text_app_is_testing(self):
		self.assertTrue(current_app.config['TESTING'])
