# coding=utf8
"""
Copyright 2014, Julen Landa Alustiza

Licensed under the Eiffel Forum License 2.
"""

from flask import flash, redirect, url_for, render_template
from flask.ext.babel import gettext, refresh
from flask.ext.user import current_user, login_required
from datetime import datetime
from app import db
from . import blueprint
from .forms import EditPreferencesForm

@blueprint.before_app_request
def before_request():
    user = current_user
    if user.is_authenticated():
        user.last_seen = datetime.utcnow()
        db.session.add(user)
        db.session.commit()

@blueprint.route('/preferences', methods=['GET', 'POST'])
@login_required
def edit_preferences():
    form = EditPreferencesForm()
    if form.validate_on_submit():
        current_user.language = form.language.data
        db.session.add(current_user)
        db.session.commit()
        flash(gettext('Saved'))
        refresh()
        redirect(url_for('.edit_preferences'))
    form.language.data = current_user.language
    return render_template('user/preferences.html', user=current_user, form=form)
