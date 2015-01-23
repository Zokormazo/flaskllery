# coding=utf8
"""
Copyright 2014, Julen Landa Alustiza

Licensed under the Eiffel Forum License 2.
"""

import unittest
import os
from flask import current_app
from app import create_app, db

class ModelsTestCase(unittest.TestCase):
    '''test models'''

    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_app_exists(self):
        self.assertFalse(current_app is None)

    def test_app_is_testing(self):
        self.assertTrue(current_app.config['TESTING'])
