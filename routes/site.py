from flask import Blueprint, jsonify, current_app, url_for
from flask_login import login_required

site = Blueprint('site', __name__)

@site.route("/")
@login_required
def index():
    return 'index'