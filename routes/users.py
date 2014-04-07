from flask import Blueprint, jsonify, render_template
from flask_login import login_required
from flask import current_app

users = Blueprint('users', __name__)


@users.route("/users")
@users.route("/users/list")
@login_required
def users_list():
    return render_template('users_list.html')


@users.route("/users/new")
@users.route("/users/edit/<user_id>")
@login_required
def users_edit(user_id=None):
    return ''