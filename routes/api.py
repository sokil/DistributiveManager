from flask import Blueprint, jsonify
from flask import current_app
from bson.objectid import ObjectId

api = Blueprint('api', __name__)


@api.route("/api/latest")
def latest():

    # get environment list
    environment_list_cursor = current_app.connection.Environment.find()
    if environment_list_cursor is None:
        raise Exception('No environments configured')

    environment_list = {}
    for environment in environment_list_cursor:
        environment_list[str(environment['_id'])] = environment['name']

    # get max values for each environment
    result = current_app.connection.Distributive.collection.aggregate([
        {'$group': {'_id': '$environment', 'version': {'$max': '$version.number'}}}
    ])

    if int(result['ok']) is not 1:
        raise Exception('Error getting max versions of distributives')

    max_versions = {}
    for max_version in result['result']:
        environment_id = max_version['_id']
        environment_name = environment_list[str(environment_id)]
        version_number = max_version['version']

        distributive = current_app.connection.Distributive.find_one({
            'environment': ObjectId(environment_id),
            'version.number': version_number
        })

        max_versions[environment_name] = {
            'url': distributive.get_url(),
            'version': distributive['version']['caption']
        }

    return jsonify(max_versions)