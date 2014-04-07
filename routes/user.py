from flask import Blueprint, jsonify, render_template, current_app, redirect, url_for, request
from flask_login import login_required
from bson.objectid import ObjectId

user = Blueprint('user', __name__)


@user.route("/user")
@user.route("/user/list")
@login_required
def user_list():
    user_list = current_app.connection.User.find()
    return render_template('user_list.html', user_list=user_list)


@user.route("/user/new")
@user.route("/user/edit/<user_id>")
@login_required
def user_edit(user_id=None):
    if user_id:
        user_instance = current_app.connection.User.find_one({'_id': ObjectId(user_id)})
    else:
        user_instance = current_app.connection.User()

    return render_template('user_edit.html', user=user_instance)


@user.route("/user/save", methods=['POST'])
@login_required
def user_save():
    user_id = request.form['id']
    if user_id:
        user_instance = current_app.connection.User.find_one({'_id': ObjectId(user_id)})
    else:
        user_instance = current_app.connection.User()

    user_instance['email'] = request.form['email']
    user_instance.set_password(request.form['password'])
    user_instance.save()

    return redirect(url_for('user.user_edit', user_id=user_instance['_id']))