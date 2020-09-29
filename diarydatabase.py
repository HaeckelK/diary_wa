"""
"""
from typing import Optional, Dict

from database import Database, Results


class DiaryDatabase(Database):
    schema = '''CREATE TABLE IF NOT EXISTS rawdiary
                (id INTEGER PRIMARY KEY,
                rawtext TEXT,
                is_draft INT,
                is_extracted INT);'''

    def insert_rawdiary(self, id: int, rawtext: str, is_draft: int, is_extracted: int):
        params = (id, rawtext, is_draft, is_extracted)
        new_id = self.insert('''INSERT INTO rawdiary(id, rawtext, is_draft, is_extracted) VALUES(?,?,?,?)''', params)
        return new_id

    def update_rawdiary(self, id: int, rawtext: str, is_draft: int, is_extracted: int):
        params = (rawtext, is_draft, is_extracted, id)
        cursor = self.query_with_params('''
                                        UPDATE rawdiary set rawtext = ?, is_draft = ?, is_extracted = ? where id = ?;
                                        ''', params)
        cursor.close()
        return

    def upsert_rawdiary(self, id: int, rawtext: str, is_draft: int, is_extracted: int):
        cursor = self.query_with_params('''
                                        select id
                                        from rawdiary
                                        where id = ?;
                                        ''', (id, ))
        args = (id, rawtext, is_draft, is_extracted)
        if cursor.fetchone():
            self.update_rawdiary(*args)
            pass
        else:
            self.insert_rawdiary(*args)
        cursor.close()
        return

    def get_rawdiary_row(self, id):
        cursor = self.query_with_params('''select *
                                        from rawdiary
                                        where id = ?;''', (id,))
        return Results(cursor).fetchall_dict_factory()

    def get_all_dates(self):
        cursor = self.query('''SELECT id FROM rawdiary''')
        result = cursor.fetchall()
        dates = set([str(x[0]) for x in result])
        return dates
