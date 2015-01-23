# coding=utf8
"""
Copyright 2014, Julen Landa Alustiza

Licensed under the Eiffel Forum License 2.
"""

from flask.ext.wtf import Form
from flask.ext.babel import gettext
from wtforms import StringField, SubmitField, SelectMultipleField, widgets
from wtforms.validators import DataRequired, Email

class MultiCheckboxField(SelectMultipleField):
    """
    A multiple-select, except displays a list of checkboxes.

    Iterating the field will produce subfields, allowing custom rendering of
    the enclosed checkbox fields.
    """
    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()

class EditUserForm (Form):
    username = StringField(gettext('Username'))
    email = StringField(gettext('Email'))
    roles = MultiCheckboxField('roles', coerce=int)
    submit = SubmitField(gettext('Edit'))
