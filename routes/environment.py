from flask import Blueprint, jsonify, current_app, render_template, redirect, url_for, request, flash
from flask_login import login_required
from flask_babel import gettext
from bson.objectid import ObjectId

environment = Blueprint('environment', __name__)

@environment.route('/')
@environment.route('/environment')
@environment.route('/environment/list')
@login_required
def environment_list():

    # get iterator
    env_list = current_app.connection.Environment.find().sort('caption', 1)

    # paginator
    from Paginator import Paginator
    paginator = Paginator(env_list)
    paginator.set_page(request.args.get('p'))

    return render_template('environment_list.html', paginator=paginator)


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

    item['name'] = request.form['name'].strip()

    item['caption'] = request.form['caption'].strip()

    from mongokit import ValidationError
    try:
        item.save()
        flash(gettext('Successfully saved'))
    except ValidationError, e:
        flash(e.message)

    return redirect(url_for('.environment_list'))


@environment.route('/environment/delete/<environment_id>')
@login_required
def environment_delete(environment_id):
    current_app.connection.Environment\
        .find_one({'_id': ObjectId(environment_id)})\
        .delete()

    return redirect(url_for('.environment_list'))