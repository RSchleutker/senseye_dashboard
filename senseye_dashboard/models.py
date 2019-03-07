# -*- coding: utf-8 -*-
"""
Created on Sun Mar  3 19:15:47 2019

@author: Raphael
"""

from senseye_dashboard import (
        db,
        login
        )

from flask_login import UserMixin
from werkzeug.security import (
        generate_password_hash,
        check_password_hash
        )

class User(UserMixin, db.Model):
    __tablename__ = 'user'

    username = db.Column(db.String(64), primary_key = True)
    email = db.Column(db.String(64), nullable = False)
    password_hash = db.Column(db.String(256), nullable = False)
    group = db.Column(db.String(32), nullable = False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def get_id(self):
        return self.username

@login.user_loader
def load_user(username):
    return User.query.get(username)

class Range(db.Model):
    __tablename__ = 'ranges'

    device = db.Column(db.Integer,
                       db.ForeignKey('devices.id'),
                       primary_key = True)
    parameter = db.Column(db.String(32), primary_key = True)
    lower = db.Column(db.Float, nullable = False)
    upper = db.Column(db.Float, nullable = False)

class Device(db.Model):
    __tablename__ = 'devices'

    id = db.Column(db.Integer, primary_key = True)
    type = db.Column(db.String(32), nullable = False)
    room = db.Column(db.String(32))
    group = db.Column(db.String(32))

class Measurement(db.Model):
    __tablename__ = 'measurements'

    device = db.Column(db.Integer,
                       db.ForeignKey('devices.id'),
                       primary_key = True)
    sensor = db.Column(db.Integer,
                       db.ForeignKey('sensors.id'),
                       primary_key = True)
    parameter = db.Column(db.String(32), primary_key = True)
    time = db.Column(db.DateTime, primary_key = True)
    value = db.Column(db.Float)

class Sensor(db.Model):
    __tablename__ = 'sensors'

    id = db.Column(db.Integer, primary_key = True)
    mac = db.Column(db.String(50), nullable = False)
    device = db.Column(db.Integer, db.ForeignKey('devices.id'))
    raspi = db.Column(db.Integer, db.ForeignKey('raspis.id'))

class RaspberryPi(db.Model):
    __tablename__ = 'raspis'

    id = db.Column(db.Integer, primary_key = True)
    room = db.Column(db.String(32), nullable = False)
    ip = db.Column(db.String(64), nullable = False, unique = True)
    port = db.Column(db.Integer, nullable = False)