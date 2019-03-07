# -*- coding: utf-8 -*-
"""
Created on Sun Mar  3 12:42:38 2019

@author: Raphael
"""

import os

from flask import (
        Flask,
        render_template
        )

from flask_sqlalchemy import SQLAlchemy
from flask_login import (
        LoginManager,
        login_required
        )

db = SQLAlchemy()
login = LoginManager()
login.login_view = 'auth.login'

BASEDIR = os.path.abspath(os.path.dirname(__file__))

def create_app(test_config = None, database = None):
    # Create and configure the app
    app = Flask(__name__, instance_relative_config = True)

    app.config.from_mapping(
            SECRET_KEY = 'dev',
            SQLALCHEMY_DATABASE_URI = database,
            SQLALCHEMY_TRACK_MODIFICATIONS = False
            )

    print(BASEDIR)

    if test_config is None:
        # Load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent = True)
    else:
        # Load the test config if passed in
        app.config.from_mapping(test_config)

    # Ensure the instance folder exists
    try:
        os.mkdir(app.instance_path)
    except OSError:
        pass

    # Register extensions with the app
    db.init_app(app)
    login.init_app(app)

    from .models import User
    with app.app_context():
        if User.query.all() == 0:
            usr = User(username = 'Username',
                       email = 'user@user.de',
                       group = 'luschnig')
            usr.set_password('password')

            db.session.add(usr)

            try:
                db.session.commit()
            except Exception as excep:
                print(excep)
            else:
                print('Successfully added default user!')

    # Register blueprints
    from . import (
            auth,
            dev,
            sen,
            rp
            )

    app.register_blueprint(auth.bp)
    app.register_blueprint(dev.bp)
    app.register_blueprint(sen.bp)
    app.register_blueprint(rp.bp)

    @app.route('/')
    @login_required
    def index():

        return render_template('index.html',
                               title = 'Welcome')

    return app