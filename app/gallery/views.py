from flask import render_template, flash, redirect, url_for, g
from flask.ext.user import login_required
from app.gallery.models import Album
from app.gallery.forms import NewAlbumForm, EditAlbumForm
from app import app, db
from config import FLASKLLERY_ALBUMS_PER_PAGE

@app.route('/')
@app.route('/index')
@app.route('/index/<int:page>')
@login_required
def index(page=1):
	albums = Album.query.paginate(page, FLASKLLERY_ALBUMS_PER_PAGE, False)
	return render_template('index.html', albums=albums)

@app.route('/album/new', methods=['GET', 'POST'])
@login_required
def new_album():
	form = NewAlbumForm()
	if form.validate_on_submit():
		album = Album(title=form.title.data, description=form.description.data, author=g.user)
		db.session.add(album)
		db.session.commit()
		flash('New album added')
		return redirect(url_for('index'))
	return render_template('new_album.html', form=form)

@app.route('/album/view/<int:id>')
@login_required
def album(id):
	album = Album.query.get(id)
	return render_template('album.html', album=album)

@app.route('/album/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_album(id):
	form = EditAlbumForm()
	album = Album.query.get(id)
	if form.validate_on_submit():
		album.title = form.title.data
		album.description = form.description.data
		db.session.add(album)
		db.session.commit()
		return redirect(url_for('album', id=album.id))
	form.title.data = album.title
	form.description.data = album.description
	return render_template('edit_album.html', album=album, form=form)

@app.route('/album/delete/<int:id>')
@login_required
def delete_album(id):
	album = Album.query.get(id)
	db.session.delete(album)
	db.session.commit()
	return redirect(url_for('index'))
