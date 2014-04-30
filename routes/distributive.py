import os
from flask import Blueprint, jsonify, render_template, request, current_app, redirect, url_for, flash, abort
from flask_login import login_required
from bson.objectid import ObjectId

distributive = Blueprint('distributive', __name__)


@distributive.route('/distributive/list/<environment_name>')
@login_required
def distributive_list(environment_name):

    # environment
    environment = current_app.connection.Environment.find_one({'name': environment_name})
    if environment is None:
        raise Exception('Environment not found')

    # distributive list
    distributives = current_app.connection.Distributive.find({'environment': environment['_id']})
    if distributives is None:
        distributives = []

    # render
    return render_template("distributive_list.html",
        environment=environment,
        distributives=distributives
    )


@distributive.route('/distributive/new/<environment_id>')
@login_required
def distributive_new(environment_id):
    # get environment_id
    environment_instance = current_app.connection.Environment.find_one({'_id': ObjectId(environment_id)})
    if environment_instance is None:
        raise Exception('Environment not found')

    # init distributive
    distributive_instance = current_app.connection.Distributive()
    distributive_instance.set_environment(environment_instance)

    return render_template('distributive_edit.html', distributive=distributive_instance)


@distributive.route('/distributive/edit/<distributive_id>')
@login_required
def distributive_edit(distributive_id):
    # get distributive
    distributive_instance = current_app.connection.Distributive.find_one({'_id': ObjectId(distributive_id)})
    if distributive_instance is None:
        raise Exception('Distributive not found')

    return render_template('distributive_edit.html', distributive=distributive_instance)


@distributive.route("/distributive/save", methods=['POST'])
@login_required
def distributive_save():

    distributive_id = request.form['id']
    if distributive_id:
        # get distributive
        distributive_instance = current_app.connection.Distributive.find_one({'_id': ObjectId(distributive_id)})

        # get environment
        environment_instance = current_app.connection.Environment.find_one({'_id': distributive_instance['environment']})
    else:
        # get environment
        environment_id = request.form['environment']
        environment_instance = current_app.connection.Environment.find_one({'_id': ObjectId(environment_id)})
        if environment_instance is None:
            raise Exception('Environment not found')

        # create distributive
        distributive_instance = current_app.connection.Distributive()
        distributive_instance.set_environment(environment_instance)

    # version
    distributive_instance.set_version(request.form['version'])

    # upload file
    if request.files['file'].filename:

        distributive_instance.set_file(request.files['file'])

    distributive_instance.save()

    flash('Successfully saved')

    return redirect(url_for('.distributive_list', environment_name=environment_instance['name']))


@distributive.route("/distributive/latest/<environment_name>")
@distributive.route("/latest/<environment_name>")
def distributive_latest(environment_name):
    # get environment
    environment = current_app.connection.Environment.find_one({'name': environment_name})
    if environment is None:
        abort(404)

    # get latest dist
    distributive_instance = environment.get_latest_distributive()
    if distributive_instance is None:
        abort(404)

    return redirect(distributive_instance.get_url())



@distributive.route('/distributive/delete/<distributive_id>')
@login_required
def distributive_delete(distributive_id):
    # get distributive
    distributive_instance = current_app.connection.Distributive.find_one({'_id': ObjectId(distributive_id)})
    if distributive_instance is None:
        raise Exception('Distributive not found')

    # get related environment
    environment_instance = current_app.connection.Environment.find_one({'_id': distributive_instance['environment']})

    # delete distributive
    distributive_instance.delete()

    return redirect(url_for('.distributive_list', environment_name=environment_instance['name']))


@distributive.route('/dl/<environment_name>/<version_caption>')
def distributive_download(environment_name, version_caption):

    # get distributive instance
    environment_instance = current_app.connection.Environment.find_one({'name': environment_name})
    distributive_instance = current_app.connection.Distributive.find_one({
        'environment': environment_instance['_id'],
        'version.caption': version_caption
    })

    # increment download counter in stat



    # redirect to download
    from flask import Response
    response = Response()
    response.headers.add('Content-Disposition', 'attachment; filename="' + distributive_instance['file'] + '"')
    response.headers.add('X-Accel-Redirect', distributive_instance.get_accel_redirect_url())
    return response

