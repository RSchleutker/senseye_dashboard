# -*- coding: utf-8 -*-
'''
Created on Sun Mar  3 20:53:04 2019

@author: Raphael
'''

from flask_wtf import FlaskForm
from wtforms import (
        StringField,
        PasswordField,
        BooleanField,
        SubmitField,
        SelectField,
        DecimalField,
        IntegerField
        )
from wtforms.validators import (
        DataRequired,
        ValidationError,
        Email,
        EqualTo
        )

ROOMS = [
        ('13', '13')
        ]

PARAMS = [
        ('humidity', 'Humidity'),
        ('temperature', 'Temperature')
        ]

GROUPS = [
        ('klaembt', 'Klämbt'),
        ('luschnig', 'Luschnig'),
        ('schirmeier', 'Schirmeier'),
        ('stanewsky', 'Stanewsky')
        ]

class LoginForm(FlaskForm):

    username = StringField('Username', validators = [DataRequired()])
    password = PasswordField('Password', validators = [DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class RegistrationForm(FlaskForm):

    username = StringField('Username', validators = [DataRequired()])
    email = StringField('Email',
                        validators = [
                                DataRequired(),
                                Email()
                                ])
    group = SelectField('Group', choices = GROUPS)
    password = PasswordField('Password', validators = [DataRequired()])
    password2 = PasswordField('Repeat Password',
                              validators = [
                                      DataRequired(),
                                      EqualTo('password')
                                      ])
    submit = SubmitField('Register')

class SensorForm(FlaskForm):

    mac = StringField('MAC Address', validators = [DataRequired()])
    device = SelectField('Device ID',
                         choices = [(0, 'None')],
                         coerce = int)
    raspi = SelectField('Raspberry Pi ID',
                        choices = [(0, 'None')],
                        coerce = int)
    submit = SubmitField('Take it')

class DeviceForm(FlaskForm):

    type = StringField('Type of Device', validators=[DataRequired()])
    room = SelectField('Room', validators=[DataRequired()], choices = ROOMS)
    group = SelectField('Group', choices = GROUPS)
    submit = SubmitField('Take it')

class RaspiForm(FlaskForm):

    room = SelectField('Room', validators = [DataRequired()],
                       choices = ROOMS)
    ip = StringField('IP Address', validators = [DataRequired()])
    port = IntegerField('Port', validators = [DataRequired()])
    submit = SubmitField('Take it')

class RangeForm(FlaskForm):

    parameter = SelectField('Parameter',
                            validators = [DataRequired()],
                            choices = PARAMS)
    lower = DecimalField('Lower Limit', validators = [DataRequired()])
    upper = DecimalField('Upper Limit', validators = [DataRequired()])
    submit = SubmitField('Take it')

class UserForm(FlaskForm):

    email = StringField('Email',
                        validators = [
                                DataRequired(),
                                Email()
                                ])
    group = SelectField('Group', choices = GROUPS)
    oldpw = PasswordField('Old Password*')
    newpw = PasswordField('New Password')
    newpw2 = PasswordField('Repeat New Password', validators = [EqualTo('newpw')])
    submit = SubmitField('Take it')