"""
Functions that will be called as scheduled or queued tasks.

For example db to db actions.
"""
import logging

from diarydatabase import DiaryDatabase

logger = logging.getlogger(__name__)


def extract_rawdiary_entries():
    db = DiaryDatabase()
    ids = db.get_unextracted_rawdiary()
    for id in ids:
        extract_rawdiary(id)
    return


def extract_rawdiary(id: int):
    
    return