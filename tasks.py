"""
Functions that will be called as scheduled or queued tasks.

For example db to db actions.
"""
import logging
import configparser

from diarydatabase import DiaryDatabase, Results

logger = logging.getLogger(__name__)


# TODO logging
# TODO DRY see app
def load_config():
    config = configparser.ConfigParser()
    config.read('config.ini')
    filename = config['DATABASE']['path']
    config = {'DBFILENAME': filename,
              'DATABASE':  DiaryDatabase(filename),
              'SECRET_KEY': 'ndgnfdksmdfpa'}
    return config

# TODO link to config
DBFILENAME = load_config()['DBFILENAME']


def extract_rawdiary_entries():
    db = DiaryDatabase(DBFILENAME)
    ids = db.get_unextracted_rawdiary()
    for id in ids:
        extract_rawdiary(id)
    return


def extract_rawdiary(id: int):
    # TODO error handling
    db = DiaryDatabase(DBFILENAME)

    data = db.get_rawdiary_row(id)[0]

    date = int(data['id'])
    rawtext = data['rawtext']
    rawtext = rawtext.replace('\n', '').replace('\r','')
    for section in rawtext.split('$')[1:]:
        category = section.split(';')[0].strip().replace(' ', '')
        original = ';'.join(section.split(';')[1:]).strip()
        db.insert_diary(date, category, original, original, is_clean=0)

    db.set_is_extracted_rawdiary(date)
    return
