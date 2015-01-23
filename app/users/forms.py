# coding=utf8
"""
Copyright 2014, Julen Landa Alustiza

Licensed under the Eiffel Forum License 2.
"""

from flask.ext.wtf import Form
from flask.ext.babel import gettext
from wtforms import StringField, SubmitField

class EditPreferencesForm(Form):
    language = StringField(gettext('Language'))
    submit = SubmitField(gettext('Save'))
