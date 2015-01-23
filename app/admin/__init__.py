# coding=utf8
"""
brain.py - Willie talking bot module
Copyright 2014, Julen Landa Alustiza

Licensed under the Eiffel Forum License 2.
"""

from flask import Blueprint

blueprint = Blueprint('admin', __name__)

from . import views
