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
    if key is None:
        return False

    return True


@api.route('/api/token')
def get_token():
    if 'app_id' not in request.args:
        abort(400)

    if 'app_key' not in request.args:
        abort(400)

    # Get key
    key = current_app.connection.Apikey.find_one({'_id': ObjectId(request.args['app_id'])})
    if key is None:
        abort(403)

    # Check key
    if key != request.args['app_key']:
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


@api.route("/api/latest/<environment_name>")
def latest_env(environment_name):

    # get environment list
    environment = current_app.connection.Environment.find_one({'name': environment_name})
    if environment is None:
        return jsonify({})

    # get max values for each environment
    try:
        distributive = current_app.connection.Distributive.find({
            'environment': environment['_id'],
        }).sort('version.number', 1).limit(1)[0]
    except IndexError, e:
        return jsonify({})

    return jsonify({
        'url': distributive.get_url(),
        'version': distributive['version']['caption']
    })


@api.route('/api/stat/download')
@api.route('/api/stat/download/<environment_name>')
@token_auth.login_required
def stat_download(environment_name=None):

    pipelines = []

    match = {}

    # time
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

    match['time'] = {
        '$gte': time_from,
        '$lte': time_to
    }

    # environment
    if environment_name:
        environment = current_app.connection.Environment.find_one({'name': environment_name})
        if not environment:
            abort(404)

        environment_collection = {str(environment['_id']): environment_name}
        match['environment_id'] = environment['_id']
    else:
        environment_collection = {}
        for env in current_app.connection.Environment.find():
            environment_collection[str(env['_id'])] = env['name']

    pipelines.append({'$match': match})

    # group by time interval
    if 'group' in request.args and request.args['group'] in ['hour', 'day', 'week', 'month']:
        group = request.args['group']
    else:
        group = None

    if group == 'hour':
        group_pipeline = {
            '$group': {
                '_id': {
                    'y': {'$year': '$time'},
                    'm': {'$month': '$time'},
                    'd': {'$dayOfMonth': '$time'},
                    'h': {'$hour': '$time'},
                    'env': '$environment_id'
                },
                'count': {'$sum': '$count'}
            }
        }
    elif group == 'day':
        group_pipeline = {
            '$group': {
                '_id': {
                    'y': {'$year': '$time'},
                    'm': {'$month': '$time'},
                    'd': {'$dayOfMonth': '$time'},
                    'env': '$environment_id'
                },
                'count': {'$sum': '$count'}
            }
        }
    elif group == 'week':
        group_pipeline = {
            '$group': {
                '_id': {
                    'y': {'$year': '$time'},
                    'w': {'$week': '$time'},
                    'env': '$environment_id'
                },
                'count': {'$sum': '$count'}
            }
        }
    elif group == 'month':
        group_pipeline = {
            '$group': {
                '_id': {
                    'y': {'$year': '$time'},
                    'm': {'$month': '$time'},
                    'env': '$environment_id'
                },
                'count': {'$sum': '$count'}
            }
        }
    else:
        group_pipeline = {
            '$group': {
                '_id': {
                    'time': '$time',
                    'env': '$environment_id'
                },
                'count': {'$sum': '$count'}
            }
        }

    pipelines.append(group_pipeline)

    # aggregate
    result = current_app.connection.DownloadStat.collection.aggregate(pipelines)

    # prepare result
    stat = {}
    total = 0
    for item in result['result']:

        item_env_name = environment_collection[str(item['_id']['env'])]
        if item_env_name not in stat:
            stat[item_env_name] = []

        if group:
            data = item['_id']
            data['count'] = item['count']
            del data['env']
            stat[item_env_name].append(data)
        else:
            item_timestamp = int(mktime(item['_id']['time'].timetuple()))
            stat[item_env_name].append({'time': item_timestamp, 'count': item['count']})

        total += item['count']

    return jsonify({
        'stat': stat,
        'total': total,
    })