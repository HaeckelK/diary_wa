from typing import Dict
import configparser

from flask import Flask, render_template, redirect, url_for, request, jsonify
import requests

from diarydatabase import DiaryDatabase


app = Flask(__name__)


@app.route('/')
def index():
    items = ('$breakfast', '$lunch', '$dinner', '$exercise', '$film', '$tv', '$game', '$journal')
    default_text = ';\n'.join(items) + ';\n'
    date = '20200927'
    return render_template('diary_index.html', default=default_text, date=date)


@app.route('/api/add_diary_entry')
def add_diary_entry():
    data = dict(request.args)
    # TODO error handling
    date = data['date']
    diary_text = data['diary_text']
    diary_text = diary_text.replace('\n', '').replace('\r','')
    data['diary_text'] = diary_text
    # TODO move this to app['config']
    config = configparser.ConfigParser()
    config.read('config.ini')
    filename = config['DATABASE']['path']
    db = DiaryDatabase(filename)
    for section in diary_text.split('$'):
        field = section.split(';')[0].strip().replace(' ', '')
        text = ';'.join(section.split(';')[1:])
        if field:
            db.add_raw_diary_entry(field, text, date, processed=0)
    return jsonify(data)
