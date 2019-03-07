# -*- coding: utf-8 -*-
"""
Created on Tue Mar  5 09:16:07 2019

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
import pandas as pd
from bokeh.plotting import figure
from bokeh.models import (
        BoxAnnotation,
        ColumnDataSource,
        HoverTool,
        #Datetime,
        DatetimeTickFormatter
        )
from bokeh.layouts import gridplot
from bokeh.embed import components
from datetime import (
        datetime,
        timedelta
        )
from .forms import (
        SensorForm
        )
from .tables import SensorTable
from senseye_dashboard.models import (
        Device,
        Measurement,
        Range,
        Sensor,
        RaspberryPi
        )
from senseye_dashboard import db


bp = Blueprint('sen', __name__, url_prefix = '/sen')

@bp.route('/sensors')
@login_required
def sensors():

    sensors = Sensor.query.order_by('raspi', 'id').all()
    table = SensorTable(sensors)

    return render_template('sen/sensors.html',
                           title = 'Sensors',
                           number = len(sensors),
                           table = table)

@bp.route('/sensor/add', methods = ["GET", "POST"])
@login_required
def add_sensor():

    form = SensorForm()

    for d in Device.query.order_by('group', 'room', 'type', 'id').all():
        form.device.choices.append((d.id, '{gr}: Room {rm} - {ty} {id}'.format(gr = d.group,
                                                                               rm = d.room,
                                                                               ty = d.type,
                                                                               id = d.id)))

    for r in RaspberryPi.query.order_by('room').all():
        form.raspi.choices.append((r.id, 'Room {rm} - IP: {ip}'.format(rm = r.room,
                                                                       ip = r.ip)))

    if form.validate_on_submit():

        db.session.add(Sensor(mac = form.mac.data,
                              device = None if form.device.data == 0 else form.device.data,
                              raspi = None if form.raspi.data == 0 else form.raspi.data))
        try:
            db.session.commit()
        except Exception as excep:
            flash(excep)
        else:
            flash('Successfully added sensor!')
            return redirect(url_for('sen.add_sensor'))

    return render_template('sen/add_edit_sensor.html',
                           title='Add Sensor',
                           form=form)

@bp.route('/sensor/edit', methods = ["GET", "POST"])
@login_required
def edit_sensor():

    id = request.args.get('id', None)

    sensor = Sensor.query.get(id)
    form = SensorForm(mac = sensor.mac,
                      device = 0 if not sensor.device else sensor.device,
                      raspi = 0 if not sensor.raspi else sensor.raspi)

    for d in Device.query.order_by('group').all():
        form.device.choices.append((d.id, '{gr}: Room {rm} - {ty} {id}'.format(gr = d.group,
                                                                               rm = d.room,
                                                                               ty = d.type,
                                                                               id = d.id)))

    for r in RaspberryPi.query.order_by('room').all():
        form.raspi.choices.append((r.id, 'Room {rm} - IP: {ip}'.format(rm = r.room,
                                                                       ip = r.ip)))

    if form.validate_on_submit():
        sensor.mac = form.mac.data
        sensor.device = None if form.device.data == 0 else form.device.data
        sensor.raspi = None if form.raspi.data == 0 else form.raspi.data

        try:
            db.session.commit()
        except Exception as excep:
            flash(excep)
        else:
            flash('Successfully edited sensor!')
            return redirect(url_for('sen.sensors'))

    return render_template('sen/add_edit_sensor.html',
                           title='Edit Sensor',
                           form=form,
                           sensor=sensor)