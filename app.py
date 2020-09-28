from typing import Dict
import configparser

from flask import Flask, render_template, redirect, url_for, request, jsonify
import requests

from diarydatabase import DiaryDatabase
import utils


def load_config():
    config = configparser.ConfigParser()
    config.read('config.ini')
    filename = config['DATABASE']['path']
    config = {'DBFILENAME': filename,
              'DATABASE':  DiaryDatabase(filename)}
    return config


app = Flask(__name__)
app.config.update(load_config())


@app.route('/')
def index():
    days = utils.last_n_days(14)
    db = app.config['DATABASE']
    completed_dates = list(db.get_all_dates())
    return render_template('diary_index.html', days=days, completed_dates=completed_dates)


@app.route('/forms/diary_entry/<date>')
def form_diary_entry(date):
    items = ('$breakfast', '$lunch', '$dinner', '$exercise', '$film', '$tv', '$game', '$journal')
    default_text = ';\n'.join(items) + ';\n'
    return render_template('form_diary_entry.html', default=default_text, date=date)


@app.route('/api/add_diary_entry')
def add_diary_entry():
    data = dict(request.args)
    # TODO error handling
    date = data['date']
    diary_text = data['diary_text']
    diary_text = diary_text.replace('\n', '').replace('\r','')
    data['diary_text'] = diary_text

    db = app.config['DATABASE']
    for section in diary_text.split('$'):
        field = section.split(';')[0].strip().replace(' ', '')
        text = ';'.join(section.split(';')[1:])
        if field:
            db.add_raw_diary_entry(field, text, date, processed=0)
    return redirect(url_for('index'))



