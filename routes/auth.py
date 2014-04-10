from flask import Blueprint, jsonify, render_template, current_app, redirect, url_for, flash, request
from flask_login import login_required, login_user, logout_user
from flask_babel import gettext
from models.user import User

auth = Blueprint('auth', __name__)

@auth.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        user = current_app.connection.User.find_one({u'email': request.form['email'].strip()})

        if user is None:
            flash(gettext(u'Email wrong'))
            return redirect(url_for('auth.login'))

        if not user.has_password(request.form['password'].strip()):
            flash(gettext(u'Password wrong'))
            return redirect(url_for('auth.login'))

        login_user(user)
        return redirect(url_for('environment.environment_list'))


@auth.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect('/')


@auth.route("/hash")
@login_required
def password_hash():
    password = request.args.get('p', '')
    salt = request.args.get('s', '')

    return jsonify({
        'password': password,
        'hash': User.get_password_hash(password, salt),
        'salt' : salt
    })