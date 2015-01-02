from flask.ext.wtf import Form
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length

class NewAlbumForm(Form):
	title = StringField('Title', validators=[DataRequired(), Length(3, 64)])
	description = StringField('Description', validators=[Length(0, 255)])
	submit = SubmitField('Add')

class EditAlbumForm(Form):
	title = StringField('Title', validators=[DataRequired(), Length(3, 64)])
	description = StringField('Description', validators=[Length(0, 255)])
	submit = SubmitField('Edit')

class AddDirectoryForm(Form):
	path = StringField('Path')
	submit = SubmitField('Add')
