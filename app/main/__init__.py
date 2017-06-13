__author__ = 'ash975@live.com'

from flask import Blueprint

main = Blueprint('main', __name__)

from . import views
from . import errors