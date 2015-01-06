from flask import Blueprint

blueprint = Blueprint('gallery', __name__)

from . import views
