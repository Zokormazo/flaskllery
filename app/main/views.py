# coding=utf8
"""
Copyright 2014, Julen Landa Alustiza

Licensed under the Eiffel Forum License 2.
"""

from flask import redirect, request, url_for, g
from .. import babel
from . import blueprint

@blueprint.route('/')
def index():
    return redirect(url_for('gallery.index'))

@babel.localeselector
def get_locale():
    translations = [str(translation) for translation in babel.list_translations()]
    return request.accept_languages.best_match(translations)

@blueprint.before_app_request
def before_app_request():
    g.locale = get_locale()
