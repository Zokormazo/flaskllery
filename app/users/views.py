from flask import g
from flask.ext.user import current_user
from datetime import datetime
from app import db
from . import blueprint

@blueprint.before_request
def before_request():
	g.user = current_user
	if g.user.is_authenticated():
		g.user.last_seen = datetime.utcnow()
		db.session.add(g.user)
		db.session.commit()

