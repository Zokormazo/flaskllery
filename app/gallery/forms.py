from flask.ext.wtf import Form
from flask.ext.babel import gettext
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length, ValidationError
import os

def directory_path_validator(form, field):
	path = field.data
	if not os.path.isdir(path):
		raise ValidationError(gettext('Path is not a valid directory. Please try with a valid directory path'))

class NewAlbumForm(Form):
	title = StringField(gettext('Title'), validators=[DataRequired(), Length(3, 64)])
	description = StringField(gettext('Description'), validators=[Length(0, 255)])
	submit = SubmitField(gettext('Add'))

class EditAlbumForm(Form):
	title = StringField(gettext('Title'), validators=[DataRequired(), Length(3, 64)])
	description = StringField(gettext('Description'), validators=[Length(0, 255)])
	submit = SubmitField(gettext('Edit'))

class AddDirectoryForm(Form):
	path = StringField(gettext('Path'), validators=[DataRequired(), directory_path_validator])
	submit = SubmitField(gettext('Add'))

class EditPhotoForm(Form):
	title = StringField(gettext('Title'))
	caption = StringField(gettext('Caption'))
	submit = SubmitField(gettext('Edit'))
