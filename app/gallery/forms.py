from flask.ext.wtf import Form
from flask.ext.babel import gettext
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length

class NewAlbumForm(Form):
	title = StringField('Title', validators=[DataRequired(), Length(3, 64)])
	description = StringField('Description', validators=[Length(0, 255)])
	submit = SubmitField(gettext('Add'))

class EditAlbumForm(Form):
	title = StringField('Title', validators=[DataRequired(), Length(3, 64)])
	description = StringField('Description', validators=[Length(0, 255)])
	submit = SubmitField(gettext('Edit'))

class AddDirectoryForm(Form):
	path = StringField('Path')
	submit = SubmitField(gettext('Add'))

class EditPhotoForm(Form):
	title = StringField('Title')
	caption = StringField('Caption')
	submit = SubmitField(gettext('Edit'))
