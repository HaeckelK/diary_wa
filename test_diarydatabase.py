import pytest
import os

from diarydatabase import DiaryDatabase, Results


@pytest.fixture()
def empty_database():
    db = DiaryDatabase(':memory:')
    db.initial_setup()
    return db


# TODO shouldn't pack this many tests into one place
def test_rawdiary(tmpdir):
    filename = os.path.join(tmpdir, 'test.db')
    db = DiaryDatabase(filename)
    db.initial_setup()

    db.upsert_rawdiary('20201003', 'abc', 1, 0)
    upsert_result = Results(db.query('''SELECT * FROM rawdiary''')).fetchall_dict_factory()
    assert upsert_result == db.get_rawdiary_row('20201003')

    db.upsert_rawdiary('20201003', 'abc', 0, 1)
    upsert_result = Results(db.query('''SELECT * FROM rawdiary''')).fetchall_dict_factory()
    assert upsert_result == db.get_rawdiary_row('20201003')

    db.upsert_rawdiary('20201002', 'def', 1, 0)
    dates_result = db.get_all_dates()
    assert dates_result == ['20201002', '20201003']