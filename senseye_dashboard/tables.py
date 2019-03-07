# -*- coding: utf-8 -*-
"""
Created on Mon Mar  4 14:55:43 2019

@author: Raphael
"""

from flask import (
        url_for
        )
from flask_table import (
        Table,
        Col,
        LinkCol,
        ButtonCol
        )
from senseye_dashboard.models import (
        User,
        Device,
        Range,
        Sensor,
        Measurement,
        RaspberryPi
        )
from senseye_dashboard import db
from senseye_dashboard.models import (
        Device,
        Measurement,
        Range
        )
from datetime import (
        datetime,
        timedelta
        )

class DeviceStatusCol(Col):

    def td_format(self, content):

        device = Device.query.get(content)
        ranges = Range.query.filter(Range.device == content).all()

        last_dates = []

        for rg in ranges:
            msr = Measurement.query.filter(Measurement.device == content,
                                              Measurement.parameter == rg.parameter,
                                              (Measurement.value < rg.lower) | (Measurement.value > rg.upper)).\
                                    order_by(Measurement.time.desc()).first()
            if msr:
                last_dates.append(msr.time)

        if not last_dates:
            return '<span class="badge badge-success">All fine</span>'
        elif max(last_dates) > datetime.now() - timedelta(hours=1):
            return '<span class="badge badge-danger">Alert</span>'
        elif max(last_dates) > datetime.now() - timedelta(hours=24):
            return '<span class="badge badge-warning">Attention</span>'
        else:
            return '<span class="badge badge-success">All fine</span>'

class SensorDeviceCol(Col):

    def td_format(self, content):

        sensor = Sensor.query.get(content)

        if sensor.device:
            device = Device.query.get(sensor.device)
            return '<a href="{url}" class="badge badge-info">{ty} {id}</span>'.format(url = url_for('dev.device', id=device.id),
                                                                                      ty = device.type,
                                                                                      id = device.id)
        else:
            return '<span class="badge badge-secondary">None</span>'

class SensorRaspiCol(Col):

    def td_format(self, content):

        sensor = Sensor.query.get(content)

        if sensor.raspi:
            raspi = RaspberryPi.query.get(sensor.raspi)
            return '<a href="{url}" class="badge badge-info">{id} - {ip}</span>'.format(url = url_for('rp.edit_raspi', id=raspi.id),
                                                                                      id = raspi.id,
                                                                                      ip = raspi.ip)
        else:
            return '<span class="badge badge-secondary">None</span>'


class SensorBatteryCol(Col):

    def td_format(self, content):

        battery = Measurement.query.filter(Measurement.sensor == content,
                                            Measurement.parameter == 'battery').\
                                     order_by(Measurement.time.desc()).first()

        if not battery or battery.time < datetime.now() - timedelta(days=7):
            return '<span class="badge badge-secondary">Unknown</span>'
        elif battery.value < 10:
            return '<span class="badge badge-danger">{}%</span>'.format(battery.value)
        elif battery.value < 25:
            return '<span class="badge badge-warning">{}%</span>'.format(battery.value)
        else:
            return '<span class="badge badge-success">{}%</span>'.format(battery.value)

class RaspiSensorCol(Col):

    def td_format(self, content):

        sensors = Sensor.query.filter(Sensor.raspi == content).all()

        if not sensors:
            return '<span class="badge badge-secondary">0</span>'
        else:
            badge = '<span class="badge badge-info">{n}</span> &ensp; '.format(n = len(sensors))
            sid = ', '.join([str(s.id) for s in sensors])

            return badge + sid


class UserTable(Table):

    classes = ['table', 'table-striped']

    username = Col('Username')
    email = Col('Email')
    group = Col('Group')
    delete = ButtonCol('', 'auth.delete_user',
                       url_kwargs=dict(username='username'),
                       button_attrs={'class':'btn btn-danger btn-sm btn-side'},
                       text_fallback='Delete')

class DeviceTable(Table):

    classes = ['table', 'table-striped']
    no_items = 'No items!'

    status = DeviceStatusCol(name = 'Status', attr = 'id')
    id = Col('ID')
    type = Col('Type')
    group = Col('Group')
    room = Col('Room')
    details = ButtonCol('', 'dev.device',
                        url_kwargs=dict(id='id'),
                        button_attrs={'class':'btn btn-secondary btn-sm btn-side'},
                        text_fallback='Details')

class SensorTable(Table):

    classes = ['table', 'table-striped']

    id = Col('ID')
    mac = Col('MAC Address')
    device = SensorDeviceCol(name = 'Device', attr = 'id')
    raspi = SensorRaspiCol(name = 'Raspberry Pi', attr = 'id')
    battery = SensorBatteryCol(name = 'Battery', attr = 'id')
    edit = ButtonCol('', 'sen.edit_sensor',
                     url_kwargs=dict(id='id'),
                     button_attrs={'class':'btn btn-secondary btn-sm btn-side'},
                     text_fallback='Edit')

class RaspiTable(Table):

    classes = ['table', 'table-striped']

    id = Col('ID')
    room = Col('Room')
    ip = Col('IP Address')
    port = Col('Port')
    sensors = RaspiSensorCol(name = 'Sensors', attr = 'id')
    edit = ButtonCol('', 'rp.edit_raspi',
                     url_kwargs=dict(id='id'),
                     button_attrs={'class':'btn btn-secondary btn-sm btn-side'},
                     text_fallback='Edit')
