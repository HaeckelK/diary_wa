import pytest
import os

from diarydatabase import DiaryDatabase, Results, BookNotesDatabase


def test_rawdiary(tmpdir):
    filename = os.path.join(tmpdir, 'test.db')
    db = DiaryDatabase(filename)
    db.initial_setup()

    db.upsert_rawdiary('20201003', 'abc', 1, 0)
    upsert_result = Results(db.query('''SELECT * FROM rawdiary''')).fetchall_dict_factory()
    assert upsert_result == db.get_rawdiary_row('20201003')
    assert db.get_rawdiary_status(20201003) == 1

    db.upsert_rawdiary('20201003', 'abc', 0, 1)
    upsert_result = Results(db.query('''SELECT * FROM rawdiary''')).fetchall_dict_factory()
    assert upsert_result == db.get_rawdiary_row('20201003')

    db.upsert_rawdiary('20201002', 'def', 0, 0)
    dates_result = db.get_all_dates()
    assert dates_result == ['20201002', '20201003']

    assert db.get_all_rawdiary() == [{'id': 20201002, 'is_draft': 0, 'is_extracted': 0, 'rawtext': 'def'},
                                     {'id': 20201003, 'is_draft': 0, 'is_extracted': 1, 'rawtext': 'abc'}]

    assert db.get_unextracted_rawdiary() == ['20201002']

    db.delete_rawdiary(20201003)
    db.set_is_extracted_rawdiary(20201002)
    assert db.get_all_rawdiary() == [{'id': 20201002, 'is_draft': 0, 'is_extracted': 1, 'rawtext': 'def'}]


def test_diary(tmpdir):
    filename = os.path.join(tmpdir, 'test.db')
    db = DiaryDatabase(filename)
    db.initial_setup()

    db.insert_diary(20201003, 'journal', 'abc', 'abc', 0)
    assert db.diary_get_all() == [{'id': 1, 'diary_date': 20201003, 'category': 'journal', 'original': 'abc', 'clean': 'abc', 'is_clean': 0}]
    db.insert_diary(20201002, 'film', 'def', 'def', 0)
    assert db.diary_get_categories() == ['journal', 'film']
    assert db.diary_get_all_category('film') == [{'id': 2, 'diary_date': 20201002, 'category': 'film', 'original': 'def', 'clean': 'def', 'is_clean': 0}]
    assert db.diary_for_date(20201003) == [{'id': 1, 'diary_date': 20201003, 'category': 'journal', 'original': 'abc', 'clean': 'abc', 'is_clean': 0}]


def test_book(tmpdir):
    filename = os.path.join(tmpdir, 'test.db')
    db = BookNotesDatabase(filename)
    db.initial_setup()

    db.insert_book('abc')
    db.insert_book('def', '123')
    assert db.book_get_all() == [{'id': 1, 'title': 'abc', 'isbn': None},
                                 {'id': 2, 'title': 'def', 'isbn': '123'}]
    assert db.get_book(2) == {'id': 2, 'title': 'def', 'isbn': '123'}


def test_chapternotes(tmpdir):
    filename = os.path.join(tmpdir, 'test.db')
    db = BookNotesDatabase(filename)
    db.initial_setup()

    db.insert_chapternotes(999, 27, 'begin', 'not my cup of tea')
    assert db.chapternotes_get_all() == [{'id': 1, 'book_id': 999, 'chapter': 27, 'chapter_title': 'begin', 'notes': 'not my cup of tea'}]
    db.insert_chapternotes(100, 10, 'end', 'still not my cup of tea')
    db.upsert_chapternotes(1, 999, 27, 'begin', 'nope')
    assert db.get_chapter(1) == {'id': 1, 'book_id': 999, 'chapter': 27, 'chapter_title': 'begin', 'notes': 'nope'}
    assert db.book_get_chapternotes(999) == [{'id': 1, 'book_id': 999, 'chapter': 27, 'chapter_title': 'begin', 'notes': 'nope'}]
