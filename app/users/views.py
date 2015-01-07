from flask import g
from flask.ext.user import current_user
from datetime import datetime
from app import db
from . import blueprint

@blueprint.before_app_request
def before_request():
	user = current_user
	if user.is_authenticated():
		user.last_seen = datetime.utcnow()
		db.session.add(user)
		db.session.commit()

