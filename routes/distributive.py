from flask import Blueprint, jsonify
from flask import current_app

api = Blueprint('distributive', __name__)


@api.route("/distributive/save")
def index():
    distributive = current_app.connection.Distributive()
    distributive['url'] = 'hhhhhhh'
    distributive['version'] = 'v0.10'
    distributive.save()

    return jsonify({'error': 0})