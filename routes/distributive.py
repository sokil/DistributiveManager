import os
from flask import Blueprint, jsonify, render_template, request, current_app, redirect, url_for, flash
from flask_login import login_required
from bson.objectid import ObjectId

distributive = Blueprint('distributive', __name__)


@distributive.route('/distributive/list/<environment_name>')
@login_required
def distributive_list(environment_name):

    print current_app.config['SERVER_NAME']

    # environment
    environment=current_app.connection.Environment.find_one({'name': environment_name})
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
        distributive_instance = current_app.connection.Distributive.find_one({'_id': ObjectId(distributive_id)})
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

    return redirect(url_for('distributive.distributive_edit', distributive_id=distributive_instance['_id']))