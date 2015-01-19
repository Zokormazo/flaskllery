from flask import render_template, current_app, flash, redirect, url_for
from flask.ext.user import roles_required
from flask.ext.babel import gettext
from . import blueprint
from .forms import EditUserForm
from ..models import User, Role
from .. import db

@blueprint.route('/')
@blueprint.route('/index')
@roles_required('admin')
def index():
	''' Admin dashboard index '''
	return render_template('admin/index.html')

@blueprint.route('/members')
@blueprint.route('/members/<int:page>')
@roles_required('admin')
def members(page=1):
	''' Show members '''
	users = User.query.paginate(page, current_app.config['FLASKLLERY_USERS_PER_PAGE'], False)
	return render_template('admin/members.html', members=users)

@blueprint.route('/user/<int:id>')
@roles_required('admin')
def user(id):
	''' Show user '''
	user = User.query.get_or_404(id)
	return render_template('admin/user.html', user=user)

@blueprint.route('/user/<int:id>/edit', methods=['GET', 'POST'])
@roles_required('admin')
def edit_user(id):
	''' Edit user '''
	user = User.query.get_or_404(id)
	form = EditUserForm()
	form.roles.choices = [(x.id,x.name) for x in Role.query.all()]
	if form.validate_on_submit():
		user.username = form.username.data
		user.email = form.email.data
		for role in user.roles:
			user.roles.remove(role)
		for role_id in form.roles.data:
			role = Role.query.get(role_id)
			if role is not None:
				if role not in user.roles:
					user.roles.append(role)
		db.session.add(user)
		db.session.commit()
		flash(gettext('User \'%(user)s\' edited', user=user.username))
		return redirect(url_for('.members'))
	form.username.data = user.username
	form.email.data = user.email
	form.roles.data = [role.id for role in user.roles]
	return render_template('admin/edit_user.html', user=user, form=form)


@blueprint.route('/user/<int:id>/delete')
@roles_required('admin')
def delete_user(id):
	''' Delete user '''
	user = User.query.get_or_404(id)
	db.session.delete(user)
	db.session.commit()
	flash(gettext('User \'%(user)s\' deleted', user=user.username))
	redirect(url_for('.members'))
