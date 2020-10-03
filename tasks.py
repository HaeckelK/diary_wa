"""
Functions that will be called as scheduled or queued tasks.

For example db to db actions.
"""
from diarydatabase import DiaryDatabase


def extract_rawdiary():
    db = DiaryDatabase()
    ids = db.get_unextracted_rawdiary()
    return