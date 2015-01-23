# coding=utf8
"""
Copyright 2014, Julen Landa Alustiza

Licensed under the Eiffel Forum License 2.
"""

from flask import Blueprint

blueprint = Blueprint('main', __name__)

from . import views, errors
