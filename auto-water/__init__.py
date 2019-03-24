import os
from pathlib import Path

from flask import (
    Flask, Blueprint, flash, g, redirect, render_template, request, url_for
)
from tinydb import TinyDB, Query

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    home_dir = str(Path.home())
    db = TinyDB(os.path.join(home_dir, 'config_db.json'))
    config_db = db.table('config', cache_size=0)

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

    return app
