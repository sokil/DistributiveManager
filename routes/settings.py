from flask import Blueprint, jsonify
from flask import current_app, jsonify, abort, request, render_template, redirect, url_for, flash
from bson.objectid import ObjectId
from flask_babel import gettext

settings = Blueprint('settings', __name__)


@settings.route('/settings')
def settings_index():
    return redirect(url_for('.apikey_list'))


@settings.route("/settings/apikeys")
def apikey_list():
    key_list = current_app.connection.Apikey.find()
    return render_template('apikey_list.html', key_list=key_list)


@settings.route("/settings/apikey/new")
def apikey_new():
    apikey_instance = current_app.connection.Apikey()
    return render_template('apikey_edit.html', apikey=apikey_instance)


@settings.route("/settings/apikey/edit/<id>")
def apikey_edit(id):
    apikey_instance = current_app.connection.Apikey.find_one({'_id': ObjectId(id)})
    if apikey_instance is None:
        abort(404)

    return render_template('apikey_edit.html', apikey=apikey_instance)


@settings.route('/settings/apikey/save', methods=['POST'])
def apikey_save():
    if request.form.get('id'):
        apikey_instance = current_app.connection.Apikey.find_one({'_id': ObjectId(request.form.get('id'))})
        if not apikey_instance:
            abort(404)
    else:
        apikey_instance = current_app.connection.Apikey()

    apikey_instance['name'] = request.form.get('name')

    apikey_instance.save()

    flash(gettext('Successfully saved'))

    return redirect(url_for('.apikey_list'))


@settings.route("/settings/apikey/delete/<id>")
def apikey_delete(id):
    apikey_instance = current_app.connection.Apikey.find_one({'_id': ObjectId(id)})
    if apikey_instance is None:
        abort(404)

    apikey_instance.delete()

    flash(gettext('Successfully deleted'))

    return redirect(url_for('.apikey_list'))


@settings.route("/settings/apikey/regenerate/<id>")
def apikey_regenerate(id):
    apikey_instance = current_app.connection.Apikey.find_one({'_id': ObjectId(id)})
    if apikey_instance is None:
        abort(404)

    apikey_instance.regenerate_key()

    flash(gettext('Key successfully regenerated'))

    return redirect(url_for('.apikey_list'))

