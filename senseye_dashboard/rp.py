# -*- coding: utf-8 -*-
"""
Created on Tue Mar  5 17:51:46 2019

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
        RaspiForm
        )
from .tables import RaspiTable
from senseye_dashboard.models import (
        Device,
        Measurement,
        Range,
        Sensor,
        RaspberryPi
        )
from senseye_dashboard import db


bp = Blueprint('rp', __name__, url_prefix = '/raspberrypis')

@bp.route('/')
@login_required
def raspis():

    raspis = RaspberryPi.query.order_by('room').all()
    table = RaspiTable(raspis)

    return render_template('rp/raspis.html',
                           title = 'RaspberryPis',
                           number = len(raspis),
                           table = table)

@bp.route('/add', methods = ["GET", "POST"])
@login_required
def add_raspi():

    form = RaspiForm()

    if form.validate_on_submit():

        db.session.add(RaspberryPi(room = form.room.data,
                                   ip = form.ip.data,
                                   port = form.port.data))
        try:
            db.session.commit()
        except Exception as excep:
            flash(excep)
        else:
            flash('Successfully added RaspberryPi!')
            return redirect(url_for('rp.add_raspi'))

    return render_template('rp/add_edit_raspi.html',
                           title='Add RaspberryPi',
                           form=form)

@bp.route('/edit', methods = ["GET", "POST"])
@login_required
def edit_raspi():

    id = request.args.get('id', None)

    raspi = RaspberryPi.query.get(id)
    form = RaspiForm(room = raspi.room,
                     ip = raspi.ip,
                     port = raspi.port)

    if form.validate_on_submit():
        raspi.room = form.room.data
        raspi.ip = form.ip.data
        raspi.port = form.port.data

        try:
            db.session.commit()
        except Exception as excep:
            flash(excep)
        else:
            flash('Successfully edited RaspberryPi!')
            return redirect(url_for('rp.raspis'))

    return render_template('rp/add_edit_raspi.html',
                           title='Edit RaspberryPi',
                           form=form,
                           raspi=raspi)