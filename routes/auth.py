from flask import Blueprint, jsonify, render_template, current_app, redirect, request, url_for, flash
from flask_login import login_required, login_user, logout_user

auth = Blueprint('auth', __name__)

@auth.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        user = current_app.connection.User.find_one({u'email': request.form['email']})

        if user is None:
            flash('Email wrong')
            return redirect(url_for('auth.login'))

        if not user.has_password(request.form['password']):
            flash('Password wrong')
            return redirect(url_for('auth.login'))

        login_user(user)
        return redirect(url_for('site.index'))


@auth.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect('/')