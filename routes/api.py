from flask import Blueprint, jsonify
from flask import current_app, jsonify, abort, request
from bson.objectid import ObjectId

api = Blueprint('api', __name__)

# auth
from TokenAuth import TokenAuthReader
token_auth = TokenAuthReader()

@token_auth.data_verifier
def verify_data(data):
    key = current_app.connection.Apikey.find_one({'_id': ObjectId(data['key_id'])})
    print key
    if key is None:
        return False

    return True


@api.route('/api/token')
def get_token():
    if 'api_key' not in request.args:
        abort(400)

    key = current_app.connection.Apikey.find_one({'key': request.args['api_key']})
    if key is None:
        abort(403)

    from TokenAuth import TokenAuthGenerator
    generator = TokenAuthGenerator()
    generator.set_data({'key_id': str(key['_id'])})

    return jsonify({
        'token': generator.get_token()
    })


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


@api.route('/api/stat/download/<environment_name>')
@token_auth.login_required
def stat_download(environment_name):

    # environment
    environment = current_app.connection.Environment.find_one({'name': environment_name})
    if environment is None:
        abort(404)

    # get max values for each environment
    from datetime import datetime
    from time import mktime

    if 'time_from' in request.args:
        time_from = datetime.fromtimestamp(float(request.args.get('time_from')))
    else:
        time_from = datetime.today().replace(hour=0, minute=0, second=0, microsecond=0)

    if 'time_to' in request.args:
        time_to = datetime.fromtimestamp(float(request.args.get('time_to')))
    else:
        time_to = datetime.today().replace(hour=23, minute=59, second=59, microsecond=0)

    result = current_app.connection.DownloadStat.collection.aggregate([
        {
            '$match': {
                'environment_id': environment['_id'],
                'time': {
                    '$gte': time_from,
                    '$lte': time_to
                }
            },
        }, {
            '$group': {
                '_id': '$time',
                'count': {'$sum': '$count'}
            }
        }, {
            '$sort': {'_id': 1}
        }
    ])

    stat = {}
    total = 0
    for item in result['result']:
        stat[int(mktime(item['_id'].timetuple()))] = item['count']
        total += item['count']

    return jsonify({
        'stat': stat,
        'total': total,
    })