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
    n = request.args.get('n')
    try:
        n = int(n)
    except TypeError:
        n = 7

    days = utils.last_n_days(n)
    db = app.config['DATABASE']
    completed_dates = list(db.get_all_dates())

    dates = []
    for day in days:
        if day not in completed_dates:
            status = 'not_started'
        else:
            draft = db.get_rawdiary_status(day)
            if draft == 1:
                status = 'draft'
            else:
                status = 'completed'
        dates.append((day, status))

    return render_template('diary_index.html', dates=dates)


@app.route('/forms/diary_entry/<date>')
def form_diary_entry(date):
    db = app.config['DATABASE']
    row = db.get_rawdiary_row(date)
    try:
        diary_text = row[0]['rawtext']
    except (KeyError, IndexError):
        items = ('$breakfast', '$lunch', '$dinner', '$exercise', '$film', '$tv', '$game', '$journal')
        diary_text = ';\n'.join(items) + ';\n' 
    return render_template('form_diary_entry.html', text=diary_text, date=date)


@app.route('/api/add_diary_entry/')
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


@app.route('/api/add_rawdiary_entry/')
def add_rawdiary_entry():
    # TODO error handling
    id = int(request.args['id'])
    rawtext = request.args['rawtext']
    is_draft = request.args['is_draft']
    db = app.config['DATABASE']
    db.upsert_rawdiary(id, rawtext, is_draft, is_extracted=0)
    return redirect(url_for('index'))
