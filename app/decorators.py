from flask import current_app, abort
from flask.ext.user import current_user
from models import Album, Photo, Directory
from functools import wraps

def can_edit(type):
	''' check if user can edit the element '''
	def wrap(func):
		@wraps(func)
		def decorated_view(*args, **kwargs):
			id = kwargs['id']
			# get element
			if type == Album:
				element = Album.query.get_or_404(id)
			elif type == Photo:
				element = Photo.query.get_or_404(id)
			elif type == Directory:
				element = Directory.query.get_or_404(id)
				element = element.album
			else:
				return abort(404)
			# user must be logged
			if not current_user.is_authenticated():
				return current_app.user_manager.unauthenticated_view_function()
			# user must be admin or poweruser and author of element
			if not ( current_user.has_roles('admin') or ( current_user.has_roles('poweruser') and element.author == current_user )):
				return current_app.user_manager.unauthenticated_view_function()
			return func(*args, **kwargs)
	
		return decorated_view
	return wrap
