from flask import Blueprint

recipients = Blueprint('recipients', __name__)

from . import views
