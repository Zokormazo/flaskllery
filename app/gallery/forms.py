from flask.ext.wtf import Form
from flask.ext.babel import gettext
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length

class NewAlbumForm(Form):
	title = StringField(gettext('Title'), validators=[DataRequired(), Length(3, 64)])
	description = StringField(gettext('Description'), validators=[Length(0, 255)])
	submit = SubmitField(gettext('Add'))

class EditAlbumForm(Form):
	title = StringField(gettext('Title'), validators=[DataRequired(), Length(3, 64)])
	description = StringField(gettext('Description'), validators=[Length(0, 255)])
	submit = SubmitField(gettext('Edit'))

class AddDirectoryForm(Form):
	path = StringField(gettext('Path'))
	submit = SubmitField(gettext('Add'))

class EditPhotoForm(Form):
	title = StringField(gettext('Title'))
	caption = StringField(gettext('Caption'))
	submit = SubmitField(gettext('Edit'))
