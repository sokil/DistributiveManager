from flask import Blueprint, jsonify
from flask import current_app, jsonify, abort, request, render_template, redirect, url_for, flash
from bson.objectid import ObjectId

apikey = Blueprint('apikey', __name__)


@apikey.route("/apikeys")
def apikey_list():
    key_list = current_app.connection.Apikey.find()
    return render_template('apikey_list.html', key_list=key_list)

@apikey.route("/apikey/new")
def apikey_new():
    apikey_instance = current_app.connection.Apikey()
    return render_template('apikey_edit.html', apikey=apikey_instance)

@apikey.route("/apikey/edit/<id>")
def apikey_edit(id):
    apikey_instance = current_app.connection.Apikey.find_one({'_id': ObjectId(id)})
    if apikey_instance is None:
        abort(404)

    return render_template('apikey_edit.html', apikey=apikey_instance)

@apikey.route('/apikey/save', methods=['POST'])
def apikey_save():
    if request.form.get('id'):
        apikey_instance = current_app.connection.Apikey.find_one({'_id': ObjectId(request.form.get('id'))})
        if not apikey_instance:
            abort(404)
    else:
        apikey_instance = current_app.connection.Apikey()

    apikey_instance['name'] = request.form.get('name')

    apikey_instance.save()

    flash('Successfully saved')

    return redirect(url_for('.apikey_list'))

