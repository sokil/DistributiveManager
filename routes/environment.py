from flask import Blueprint, jsonify, current_app, render_template
from flask_login import login_required

environment = Blueprint('environment', __name__)

@environment.route('/')
@environment.route('/environment')
@environment.route('/environment/list')
@login_required
def environment_list():
    return render_template('environment_list.html',
        list=current_app.connection.Environment.find()
    )