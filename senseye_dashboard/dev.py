# -*- coding: utf-8 -*-
"""
Created on Mon Mar  4 15:24:36 2019

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
        DeviceForm,
        RangeForm
        )
from .tables import DeviceTable
from senseye_dashboard.models import (
        Device,
        Measurement,
        Range,
        Sensor
        )
from senseye_dashboard import db


bp = Blueprint('dev', __name__, url_prefix = '/devices')

@bp.route('')
@login_required
def devices():

    devices = Device.query.order_by('group', 'room', 'type', 'id').all()
    table = DeviceTable(devices)

    return render_template('dev/devices.html',
                           title = 'Devices',
                           number = len(devices),
                           table = table)

@bp.route('/', methods = ["GET", "POST"])
@login_required
def device():

    id = request.args.get('id', None)

    device = Device.query.get(id)
    ranges = Range.query.filter(Range.device == id).all()
    sensors = Sensor.query.filter(Sensor.device == id).all()

    # Add the latest measured battery value to each sensor
    for sensor in sensors:
        battery = Measurement.query.filter(Measurement.sensor == sensor.id,
                                           Measurement.parameter == 'battery').\
                                    order_by(Measurement.time.desc()).first()
        if battery:
            sensor.battery = battery.value
        else:
            sensor.battery = 'NA'

    # Create a list of plots
    plots = []
    for rg in ranges:
        msrs = Measurement.query.filter(Measurement.device == id,
                                        Measurement.parameter == rg.parameter).\
                                order_by(Measurement.time).all()

        plots.append(make_plot(parameter = rg.parameter.capitalize(),
                               time = [msr.time for msr in msrs],
                               value = [msr.value for msr in msrs],
                               sensor = [msr.sensor for msr in msrs],
                               lower = rg.lower,
                               upper = rg.upper))

    # Link the x_range of each plot together
    i = 0
    for plot in plots:
        plot.x_range = plots[0].x_range

    # Create a grid of the plots
    grid = gridplot(plots,
                    ncols = 1,
                    toolbar_location='right',
                    plot_height=200)

    return render_template('dev/device.html',
                           title = 'Device ' + str(id),
                           device = device,
                           ranges = ranges,
                           sensors = sensors,
                           plots = components(grid))

@bp.route('/add', methods = ["GET", "POST"])
@login_required
def add_device():

    form = DeviceForm()

    if form.validate_on_submit():
        db.session.add(Device(type=form.type.data,
                              room=form.room.data,
                              group=form.group.data))
        try:
            db.session.commit()
        except Exception as excep:
            flash(excep)
        else:
            flash('Successfully added device!')
            return redirect(url_for('dev.add_device'))

    return render_template('dev/add_edit_device.html',
                           title='Add Device',
                           form=form)

@bp.route('/edit', methods = ["GET", "POST"])
@login_required
def edit_device():

    id = request.args.get('id', None)

    device = Device.query.get(id)
    form = DeviceForm(type=device.type,
                      room=device.room,
                      group=device.group)

    if form.validate_on_submit():
        device.type = form.type.data
        device.room = form.room.data
        device.group = form.group.data

        try:
            db.session.commit()
        except Exception as excep:
            flash(excep)
        else:
            flash('Successfully edited device!')
            return redirect(url_for('dev.device', id = id))

    return render_template('dev/add_edit_device.html',
                           title='Edit Device',
                           form=form,
                           device=device)

@bp.route('/add_range', methods = ["GET", "POST"])
@login_required
def add_range():

    id = request.args.get('device', None)

    device = Device.query.get(id)
    form = RangeForm()

    if form.validate_on_submit():
        db.session.add(Range(device = id,
                             parameter = form.parameter.data,
                             lower = form.lower.data,
                             upper = form.upper.data))

        try:
            db.session.commit()
        except Exception as excep:
            flash(excep)
        else:
            flash('Successfully edited device!')
            return redirect(url_for('dev.device', id = id))

    return render_template('dev/add_edit_range.html',
                           title='Add Range',
                           form=form,
                           device=device)

@bp.route('/edit_range', methods = ["GET", "POST"])
@login_required
def edit_range():

    device = request.args.get('device', None)
    param = request.args.get('param', None)

    rg = Range.query.get((device, param))
    form = RangeForm(device = device,
                     parameter = param,
                     lower = rg.lower,
                     upper = rg.upper)

    if form.validate_on_submit():
        rg.lower = form.lower.data
        rg.upper = form.upper.data

        try:
            db.session.commit()
        except Exception as excep:
            flash(excep)
        else:
            flash('Successfully edited range!')
            return redirect(url_for('dev.device', id = device))

    return render_template('dev/add_edit_range.html',
                           title='Edit Range',
                           form=form,
                           rg=rg)

@bp.route('/delete_range', methods = ["GET", "POST"])
@login_required
def delete_range():

    device = request.args.get('device', None)
    param = request.args.get('param', None)

    rg = Range.query.get((device, param))

    db.session.delete(rg)

    try:
        db.session.commit()
    except Exception as excep:
        flash(excep)
    else:
        flash('Successfully deleted range!')

    return redirect(url_for('dev.device', id = device))

def make_plot(parameter, time, value, sensor, lower, upper):

    # Create an empty plot
    plot = figure(plot_height = 200,
                  title = parameter,
                  x_axis_type = "datetime",
                  sizing_mode = "scale_width",
                  tools = "pan,xwheel_zoom,box_zoom,reset",
                  x_range = (datetime.now() - timedelta(days=.5),
                             datetime.now())
                  )

    # Format the optical appearance of the plot
    plot.background_fill_color = "#ebebeb"
    plot.grid.grid_line_color = "white"
    plot.axis.axis_line_color = None

    # Format the x-axis properly
    plot.xaxis.formatter = DatetimeTickFormatter(days=["%Y-%m-%d"],
                                                 months=["%Y-%m-%d"],
                                                 hours=["%H:%M"],
                                                 minutes=["%H:%M:%S"]
                                                 )

    # Create a hover tool and add it to the plot
    hover = HoverTool(tooltips = [("Date", "@x{%Y-%m-%d %H:%M:%S}"),
                                  (parameter, "@y"),
                                  ("Sensor", "@sensor")],
                      formatters = {"x": "datetime"},
                      mode = "vline"
                      )
    plot.add_tools(hover)

    # Create a green box that indicates in-range values
    valid_box = BoxAnnotation(top = upper,
                              bottom = lower,
                              fill_alpha = .1,
                              fill_color = "green")
    plot.add_layout(valid_box)

    # Create a source
    source = ColumnDataSource(data = dict(x = time,
                                          y = value,
                                          sensor = sensor))

    # Add a line
    plot.line("x", "y", source = source, line_width = 2)

    return plot