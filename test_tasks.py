import pytest
import os

import tasks
from tasks import DiaryDatabase


def test_extract_rawdiary_entries(tmpdir, monkeypatch):
    filename = os.path.join(tmpdir, 'test.db')
    db = DiaryDatabase(filename)
    db.initial_setup()

    monkeypatch.setattr(tasks, 'DBFILENAME', filename)

    db.upsert_rawdiary('20201003', '$film;terminator\r\n$journal;Failed Sunday Times crossword.\r\n',
                       is_draft=0, is_extracted=0)

    tasks.extract_rawdiary_entries()

    assert db.query('''SELECT * FROM diary''').fetchall() == [(1, 20201003, 'film', 'terminator', 'terminator', 0),
                                                              (2, 20201003, 'journal', 'Failed Sunday Times crossword.', 'Failed Sunday Times crossword.', 0)]

    tasks.extract_rawdiary_entries()

    assert db.query('''SELECT * FROM diary''').fetchall() == [(1, 20201003, 'film', 'terminator', 'terminator', 0),
                                                              (2, 20201003, 'journal', 'Failed Sunday Times crossword.', 'Failed Sunday Times crossword.', 0)]
    