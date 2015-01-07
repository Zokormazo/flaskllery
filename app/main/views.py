from flask import redirect, url_for, current_app, request
from .. import babel
from . import blueprint

@blueprint.route('/')
def index():
	return redirect(url_for('gallery.index'))

@babel.localeselector
def get_locale():
	translations = [str(translation) for translation in babel.list_translations()]
	return request.accept_languages.best_match(translations)
