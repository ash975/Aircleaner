from flask import Flask
from flask import flash
from flask import redirect
from flask import render_template
from flask import request
from flask import redirect
from flask import url_for
from flask_login import login_user
from flask_login import logout_user
from flask_login import login_required
import subprocess

from app import User
from app import setting
from app import mongo

from . import setting
from ..forms import *

import json


def get_data_from_mongo():
    cursor = mongo.db.device_current.find()
    data = {}
    for item in cursor:
        data.update({item['device_name']: item})
    return data


def set_data_to_mongo(device_name, data):
    if data:
        set_data = {'$set': data}
    mongo.db['device_current'].update_one({'device_name': device_name}, set_data)


def clone_collection_to(source_collection, destination_collection):
    cursor = source_collection.find()
    destination_collection.remove({})
    for doc in cursor:
        destination_collection.insert(doc)


@setting.route('/device', methods=['GET', 'POST'])
@login_required
def device():
    return render_template('setting_device.html')


@setting.route('/switch', methods=['GET', 'POST'])
@login_required
def switch():
    switch_form = setting_switch_form(request.form)

    data = get_data_from_mongo()

    switch_list = {
        'fan_switch': data.get('fan').get('switch'),
        'pm25_switch': data.get('pm25').get('switch'),
        'host_switch': data.get('host').get('switch'),
        'thermometer_switch': data.get('thermometer').get('switch'),
        'oled_switch': data.get('oled').get('switch')
    }

    switch_state = {}

    for s in switch_list:
        if switch_list[s]:
            switch_state[s] = 'checked'
        else:
            switch_state[s] = ''

    switch_form.submit.id = 'submit'

    if switch_form.validate_on_submit():
        # fan_speed = switch_form.fan_speed.data
        # oled_dispaly = switch_form.oled_dispaly.data
        set_data_to_mongo('fan', {'switch': switch_form.fan_switch.data})
        set_data_to_mongo('pm25', {'switch': switch_form.pm25_switch.data})
        set_data_to_mongo('thermometer', {'switch': switch_form.thermometer_switch.data})
        set_data_to_mongo('host', {'switch': switch_form.host_switch.data})
        return redirect(url_for('.success'))

    return render_template('setting_switch.html', form=switch_form, switch_state=switch_state)


@setting.route('/network', methods=['GET', 'POST'])
@login_required
def network():
    network_form = setting_network_form(request.form)

    data = get_data_from_mongo()

    network_list = {
        'wifi_name': data.get('host').get('wifi_name'),
        'wifi_method': data.get('host').get('wifi_method'),
        'wifi_password': data.get('host').get('wifi_password')
    }

    if network_form.validate_on_submit():
        wifi_name = str(network_form.wifi_name.data)
        wifi_method = int(network_form.wifi_method.data)
        wifi_password = str(network_form.wifi_password.data)
        ip_address = str(network_form.ip_address)
        if wifi_method == 1:
            f = open('/etc/wpa_supplicant/wpa_supplicant.conf', 'w')
            wpa_config = subprocess.check_output(['wpa_passphrase', wifi_name, wifi_password]).decode()
            f.write(wpa_config)
            f.close()
            subprocess.Popen(['killall', 'wpa_supplicant'])
            subprocess.Popen(['wpa_supplicant', '-i', 'wlan0', '-c', '/etc/wpa_supplicant/wpa_supplicant.conf', '-B'])
            subprocess.Popen(['ifconfig', 'wlan0', ip_address])
        elif wifi_method == 2:
            subprocess.Popen(['killall', 'wpa_supplicant'])
            subprocess.Popen(['iw', 'dev', 'wlan0', 'connect', wifi_name, ' key 0:' + wifi_password])
            subprocess.Popen(['ifconfig', 'wlan0', ip_address])

        mongo.db['device_current'].update_one({'device_name': 'host'},
                                              {'$set': {'wifi_name': wifi_name, 'wifi_method': wifi_method,
                                                        'wifi_password': wifi_password, 'ip_address': ip_address}})
        return redirect(url_for('.processing'))

    return render_template('setting_network.html', form=network_form)


@setting.route('/safe', methods=['GET', 'POST'])
@login_required
def safe():
    safe_form = setting_safe_form(request.form)

    if safe_form.validate_on_submit():
        # username = safe_form.username.data
        password = safe_form.password.data
        repeat = safe_form.repeat.data
        if password != repeat:
            flash('两次密码不相同', 'WARNING')
            # elif mongo.db['user_current'].find_one({'username': username}) is not None:
            # mongo.db['user_current'].update_one({'username': username}, {'$set': {'username': username, 'username': username,
            #                                  'password': User.gen_password_hash(password)}})
            # flash('创建新用户', 'WARNING')
            # else:
            #     mongo.db['user_current'].insert({'username': username, 'username': username,
            #                                         'password': User.gen_password_hash(password)})
        else:
            mongo.db['user_current'].update_one({'username': 'aircleaner'},
                                                {'$set': {'password': User.gen_password_hash(password)}})
            return redirect(url_for('.success'))
        return redirect(url_for('.safe'))
    return render_template('setting_safe.html', form=safe_form)


@setting.route('/reset', methods=['GET', 'POST'])
@login_required
def reset():
    reset_form = setting_reset_form(request.form)
    if reset_form.validate_on_submit():
        clone_collection_to(mongo.db['user_default'], mongo.db['user_current'])
        clone_collection_to(mongo.db['device_default'], mongo.db['device_current'])
        return redirect(url_for('.success'))
    return render_template('setting_reset.html', form=reset_form)


@setting.route('/success', methods=['GET'])
@login_required
def success():
    return render_template('setting_success.html')


@setting.route('/processing', methods=['GET'])
@login_required
def processing():
    return render_template('setting_network_process.html')
