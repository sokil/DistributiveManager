from flask import Blueprint, jsonify, render_template, request, current_app
from flask_login import login_required

distributive = Blueprint('distributive', __name__)


@distributive.route('/distributive/list/<environment_name>')
@login_required
def distributive_list(environment_name):

    # environment
    environment=current_app.connection.Environment.find_one({'name': environment_name})
    if environment is None:
        raise Exception('Environment not found')

    # distributive list
    distributives = current_app.connection.Distributive.find({'environment': environment['_id']})
    print {'environment': environment_name}
    if distributives is None:
        distributives = []

    # render
    return render_template("distributive_list.html",
        environment=environment,
        distributives=distributives
    )


@distributive.route("/distributive/save")
def index():
    return jsonify({'error': 0})