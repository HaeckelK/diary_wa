"""
Copied in 20200823
"""
import sqlite3
from datetime import datetime
from typing import Tuple, Optional


class Results():
    def __init__(self, cursor):
        self.cursor = cursor
        return

    def fetchall_dict_factory(self):
        cursor = self.cursor
        rows = cursor.fetchall()
        output = []
        for row in rows:
            output.append(self.dict_factory(cursor, row))
        return output

    # TODO DRY remove from Database?
    @staticmethod
    def dict_factory(cursor, row):
        d = {}
        for idx, col in enumerate(cursor.description):
            d[col[0]] = row[idx]
        return d


class Database():
    schema = ""
    # TODO create one execute method

    def __init__(self, filename: str) -> None:
        self.filename = filename
        return

    def initial_setup(self) -> None:
        self.pre_setup_hook()
        self._process_schema()
        self.post_setup_hook()
        return

    def pre_setup_hook(self) -> None:
        pass

    def post_setup_hook(self) -> None:
        pass

    def _process_schema(self) -> None:
        DBFILENAME = self.filename
        with sqlite3.Connection(DBFILENAME) as connection:
            connection.execute("PRAGMA foreign_keys = 1")
            cursor = connection.cursor()
            cursor.executescript(self.schema)
        return

    def insert(self, sql: str, params: tuple) -> int:
        DBFILENAME = self.filename
        with sqlite3.Connection(DBFILENAME) as connection:
            cursor = connection.cursor()
            try:
                cursor.execute(sql, params)
                connection.commit()
                new_id = cursor.lastrowid
            except (sqlite3.IntegrityError, sqlite3.OperationalError):
                connection.rollback()
                new_id = None
        return new_id

    def query(self, sql):
        cursor = self.query_with_params(sql, ())
        return cursor

    def query_with_params(self, sql, params):
        DBFILENAME = self.filename
        with sqlite3.Connection(DBFILENAME) as conn:
            cursor = conn.cursor()
            cursor.execute(sql, params)
        return cursor

    @staticmethod
    def dict_factory(cursor, row):
        d = {}
        for idx, col in enumerate(cursor.description):
            d[col[0]] = row[idx]
        return d

    @staticmethod
    def _dates(date_added: Optional[str], date_modified: Optional[str]) -> Tuple[str, str]:
        if date_added is None:
            date_added = _today()
        if date_modified is None:
            date_modified = _today()
        return date_added, date_modified


def _today(date_format: str = '%Y%m%d') -> str:
    return datetime.today().strftime(date_format)
