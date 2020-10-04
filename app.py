from typing import Dict
import configparser

from flask import Flask, render_template, redirect, url_for, request, jsonify, flash
import requests

from diarydatabase import DiaryDatabase
import tasks as tasks_module # TODO sort this out
import utils


def load_config():
    config = configparser.ConfigParser()
    config.read('config.ini')
    filename = config['DATABASE']['path']
    config = {'DBFILENAME': filename,
              'DATABASE':  DiaryDatabase(filename),
              'SECRET_KEY': 'ndgnfdksmdfpa'}
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


@app.route('/api/rawdiary/', methods=['GET'])
def api_rawdiary():
    db = app.config['DATABASE']
    return jsonify(db.get_all_rawdiary())


@app.route('/api/rawdiary/<int:rawdiary_id>', methods=['GET'])
def get_rawdiary(rawdiary_id):
    db = app.config['DATABASE']
    return jsonify(db.get_rawdiary_row(rawdiary_id))


@app.route('/api/rawdiary/', methods=['POST', 'PUT'])
def create_rawdiary():
    # TODO error handling
    id = int(request.form['id'])
    rawtext = request.form['rawtext']
    is_draft = request.form['is_draft']
    db = app.config['DATABASE']
    db.upsert_rawdiary(id, rawtext, is_draft, is_extracted=0)
    if is_draft == '1':
        message = 'Diary entry saved as draft'
        flash(message)
        return redirect(request.headers.get("Referer"))
    else:
        message = 'Diary entry saved.'
        flash(message)
        return redirect(url_for('index'))


@app.route('/api/rawdiary/<int:rawdiary_id>', methods=['DELETE'])
def delete_rawdiary(rawdiary_id):
    # TODO any knock on effects?
    id = int(rawdiary_id)
    db = app.config['DATABASE']
    db.delete_rawdiary(id)
    flash(f'Deleted rawdiary id: {rawdiary_id}')
    return redirect(url_for('index'))


@app.route('/api/')
def api():
    return render_template('api_index.html')


@app.route('/tasks/')
def tasks():
    return render_template('task_index.html')


@app.route('/tasks/extract_rawdiary_entries/')
def extract_rawdiary_entries():
    tasks_module.extract_rawdiary_entries()
    return redirect(url_for('index'))


@app.route('/categories/')
def category_index():
    categories = app.config['DATABASE'].diary_get_categories()
    return render_template('category_index.html', categories=categories)


@app.route('/category/<category>')
def category_summary(category):
    data = app.config['DATABASE'].diary_get_all_category(category)
    return render_template('category_summary.html', category=category.title(), data=data)
