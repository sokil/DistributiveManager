from flask import Blueprint, jsonify, current_app, render_template, redirect, url_for, request, flash
from flask_login import login_required
from bson.objectid import ObjectId

environment = Blueprint('environment', __name__)

@environment.route('/')
@environment.route('/environment')
@environment.route('/environment/list')
@login_required
def environment_list():
    return render_template('environment_list.html',
        list=current_app.connection.Environment.find()
    )


@environment.route('/environment/new')
@environment.route('/environment/edit/<environment_id>')
@login_required
def environment_edit(environment_id=None):

    if environment_id is None:
        item = current_app.connection.Environment()
    else:
        item = current_app.connection.Environment.find_one({'_id': ObjectId(environment_id)})
        if item is None:
            raise Exception('Environment not found')

    return render_template('environment_edit.html', environment=item)


@environment.route('/environment/save', methods=['POST'])
@login_required
def environment_save():

    environment_id = request.form['id']
    if environment_id:
        item = current_app.connection.Environment.find_one({'_id': ObjectId(environment_id)})
        if item is None:
            raise Exception('Environment not found')
    else:
        item = current_app.connection.Environment()

    item['name'] = request.form['name']
    item.save()

    flash('Successfully saved')

    return redirect(url_for('.environment_edit', environment_id=item['_id']))