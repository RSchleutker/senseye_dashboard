# -*- coding: utf-8 -*-
"""
Created on Sun Mar  3 13:43:22 2019

@author: Raphael
"""

from senseye_dashboard import login
from flask import (
        Blueprint,
        flash,
        redirect,
        render_template,
        request,
        session,
        url_for
        )
from flask_login import (
        current_user,
        login_user,
        logout_user,
        login_required
        )
from werkzeug.security import (
        check_password_hash,
        generate_password_hash
        )
from .forms import (
        RegistrationForm,
        LoginForm
        )
from .tables import UserTable
from senseye_dashboard.models import User
from senseye_dashboard import db


bp = Blueprint('auth', __name__, url_prefix = '/auth')

@bp.route('/registration', methods = ('GET', 'POST'))
@login_required
def registration():

    form = RegistrationForm()

    if form.validate_on_submit():
        usr = User(username = form.username.data,
                   email = form.email.data,
                   group = form.group.data)
        usr.set_password(form.password.data)

        db.session.add(usr)

        try:
            db.session.commit()
        except Exception as excep:
            flash(excep)
        else:
            flash('New user added!')
            return redirect(url_for('auth.registration'))

    return render_template('auth/registration.html',
                           title = 'Registration',
                           form = form)

@bp.route('/delete', methods = ('GET', 'POST'))
@login_required
def delete_user():

    username = request.args.get('username', None)

    if len(User.query.all()) == 1:
        flash('At least one user needed!')
        return redirect(url_for('auth.users'))

    usr = User.query.get(username)

    db.session.delete(usr)

    try:
        db.session.commit()
    except Exception as excep:
        flash(excep)
    else:
        flash('Successfully deleted user!')

    return redirect(url_for('auth.users'))

@bp.route('/logout')
@login_required
def logout():

    logout_user()
    return redirect(url_for("auth.login"))

@bp.route('/login', methods = ('GET', 'POST'))
def login():

    if current_user.is_authenticated:
        return redirect(url_for('auth.registration'))

    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.get(form.username.data)

        if not user or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('auth.login'))

        login_user(user, remember=form.remember_me.data)
        return redirect(url_for('index'))

    return render_template('auth/login.html',
                           title="Login",
                           form=form)

@bp.route('/users')
@login_required
def users():

    usr = User.query.order_by('username').all()
    table = UserTable(usr)

    return render_template('auth/users.html',
                           title = 'Users',
                           number = len(usr),
                           table = table)
