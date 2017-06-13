from flask import render_template
from flask import request
from flask import Response
from flask_login import login_required
from datetime import datetime
from flask import redirect
from flask import url_for
from ..util import pm_color_class, temp_color_class

from . import main
from .. import mongo

@main.route('/')
@login_required
def index():
    cursor = mongo.db.device_current.find()
    data = {}
    for item in cursor:
        data.update({item['device_name']: item})

    if data.get('host').get('switch'):
        switch = 'ON'
        switch_class = 'btn my-circle-btn btn-success'
    else:
        switch = 'OFF'
        switch_class = 'btn my-circle-btn btn-danger'

    mode = int(data.get('fan').get('mode'))
    if mode == 1:
        mode_auto_class = 'btn my-circle-btn btn-warning'
        mode_sleep_class = 'btn my-circle-btn btn-default'
        mode_manual_class = 'btn my-circle-btn btn-default'
    elif mode == 2:
        mode_auto_class = 'btn my-circle-btn btn-default'
        mode_sleep_class = 'btn my-circle-btn btn-warning'
        mode_manual_class = 'btn my-circle-btn btn-default'
    elif mode == 3:
        mode_auto_class = 'btn my-circle-btn btn-default'
        mode_sleep_class = 'btn my-circle-btn btn-default'
        mode_manual_class = 'btn my-circle-btn btn-warning'

    device_state_index = {'indoor_air': int(data.get('pm25').get('pm25')),
                          'outdoor_air': int(data.get('pm25').get('outdoor_air')),
                          'indoor_air_class': pm_color_class(data.get('pm25').get('pm25'), 'my-circle'),
                          'outdoor_air_class': pm_color_class(data.get('pm25').get('outdoor_air'), 'btn btn-block'),
                          'temperature_class': temp_color_class(data.get('thermometer').get('temperature')),
                          'temperature': int(data.get('thermometer').get('temperature')),
                          'humidity': int(data.get('thermometer').get('temperature')),
                          'mode': int(data.get('fan').get('mode')),
                          'switch': switch,
                          'switch_class': switch_class,
                          'mode_auto_class': mode_auto_class,
                          'mode_sleep_class': mode_sleep_class,
                          'mode_manual_class': mode_manual_class}

    return render_template('index.html', device_state_index=device_state_index, current_time=datetime.utcnow())


@main.route('/about')
def about():
    return render_template('about.html')



@main.route('/setting')
@login_required
def setting():
    return redirect(url_for('setting.switch'))
