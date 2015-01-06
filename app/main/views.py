from flask import redirect, url_for
from . import blueprint

@blueprint.route('/')
def index():
	return redirect(url_for('gallery.index'))
