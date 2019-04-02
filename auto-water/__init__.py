import os

from flask import (
    Flask, Blueprint, flash, g, redirect, render_template, request, url_for, jsonify
)
from tinydb import TinyDB, Query
from tinydb_appengine.storages import EphemeralJSONStorage

# create and configure the app
app = Flask(__name__, instance_relative_config=True)
app.config.from_mapping(
    SECRET_KEY='dev',
)

db = TinyDB('config_db.json', storage=EphemeralJSONStorage)
config_db = db.table('config', cache_size=0)

Key = Query()
config_db.upsert({
    'key': 'water_state',
    'value': False
}, Key.key == 'water_state')
config_db.upsert({
    'key': 'current_moisture_value',
    'value': 700
}, Key.key == 'current_moisture_value')
config_db.upsert({
    'key': 'max_moisture_value',
    'value': 800
}, Key.key == 'max_moisture_value')
config_db.upsert({
    'key': 'water_on_threshold',
    'value': 350
}, Key.key == 'water_on_threshold')
config_db.upsert({
    'key': 'water_off_threshold',
    'value': 425
}, Key.key == 'water_off_threshold')

@app.route('/fill')
def fill_data():
    Key = Query()
    config_db.upsert({
        'key': 'water_state',
        'value': False
    }, Key.key == 'water_state')
    config_db.upsert({
        'key': 'current_moisture_value',
        'value': 700
    }, Key.key == 'current_moisture_value')
    config_db.upsert({
        'key': 'max_moisture_value',
        'value': 800
    }, Key.key == 'max_moisture_value')
    config_db.upsert({
        'key': 'water_on_threshold',
        'value': 350
    }, Key.key == 'water_on_threshold')
    config_db.upsert({
        'key': 'water_off_threshold',
        'value': 425
    }, Key.key == 'water_off_threshold')
    return "Done."


@app.route('/')
def index():
    Key = Query()
    max_moisture_value = config_db.search(Key.key == 'max_moisture_value')[0]['value']
    print(max_moisture_value)
    current_moisture_value = config_db.search(Key.key == 'current_moisture_value')[0]['value']
    print(current_moisture_value)
    current_state = {
        'water_state': config_db.search(Key.key == 'water_state')[0]['value'],
        'current_moisture_value': current_moisture_value * 100 / max_moisture_value ,
        'water_on_threshold': config_db.search(Key.key == 'water_on_threshold')[0]['value'] * 100 / max_moisture_value,
        'water_off_threshold': config_db.search(Key.key == 'water_off_threshold')[0]['value'] * 100 / max_moisture_value
    }
    return render_template('index.html', current_state=current_state)

@app.route('/readme')
def readme():
    import markdown2
    rendered_md = markdown2.markdown_path('README.md')
    return render_template('readme.html', rendered_md=rendered_md)

@app.route('/set_on_threshold/<int:threshold>')
def set_on_threshold(threshold):
    Key = Query()
    max_moisture_value = config_db.search(Key.key == 'max_moisture_value')[0]['value']
    config_db.upsert({
        'key': 'water_on_threshold',
        'value': threshold * max_moisture_value // 100
    }, Key.key == 'water_on_threshold')
    return jsonify({'status': 'success'})

@app.route('/get_on_threshold')
def get_on_threshold():
    Key = Query()
    value = config_db.search(Key.key == 'water_on_threshold')[0]['value']
    return jsonify({'status': 'success', 'value': value})

@app.route('/set_off_threshold/<int:threshold>')
def set_off_threshold(threshold):
    Key = Query()
    max_moisture_value = config_db.search(Key.key == 'max_moisture_value')[0]['value']
    config_db.upsert({
        'key': 'water_off_threshold',
        'value': threshold * max_moisture_value // 100
    }, Key.key == 'water_off_threshold')
    return jsonify({'status': 'success'})

@app.route('/get_off_threshold')
def get_off_threshold():
    Key = Query()
    value = config_db.search(Key.key == 'water_off_threshold')[0]['value']
    return jsonify({'status': 'success', 'value': value})

@app.route('/set_water_state/<state>')
def set_water_state(state):
    Key = Query()
    config_db.upsert({
        'key': 'water_state',
        'value': state == 'true'
    }, Key.key == 'water_state')
    return jsonify({'status': 'success'})

@app.route('/set_current_moisture_value/<int:value>')
def set_current_moisture_value(value):
    Key = Query()
    config_db.upsert({
        'key': 'current_moisture_value',
        'value': value
    }, Key.key == 'current_moisture_value')
    return jsonify({'status': 'success'})
