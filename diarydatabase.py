"""
"""
from typing import Optional, Dict

from database import Database, Results


class DiaryDatabase(Database):
    schema = '''CREATE TABLE IF NOT EXISTS rawdiary
                (id INTEGER PRIMARY KEY,
                rawtext TEXT,
                is_draft INT,
                is_extracted INT);
                CREATE TABLE IF NOT EXISTS diary
                (id INTEGER PRIMARY KEY,
                diary_date INT,
                category TEXT,
                original TEXT,
                clean TEXT,
                is_clean INT);'''

    def insert_rawdiary(self, id: int, rawtext: str, is_draft: int, is_extracted: int):
        params = (id, rawtext, is_draft, is_extracted)
        new_id = self.insert('''INSERT INTO rawdiary(id, rawtext, is_draft, is_extracted) VALUES(?,?,?,?)''', params)
        return new_id

    def insert_diary(self, diary_date: int, category: str, original: str, clean: str, is_clean: int):
        params = (diary_date, category, original, clean, is_clean)
        new_id = self.insert('''INSERT INTO diary(diary_date, category, original, clean, is_clean) VALUES(?,?,?,?,?)''', params)
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
        dates = list([str(x[0]) for x in result])
        return dates

    def get_all_rawdiary(self):
        cursor = self.query('''select *
                               from rawdiary''')
        return Results(cursor).fetchall_dict_factory()

    def delete_rawdiary(self, id):
        cursor = self.query_with_params('''delete
                                        from rawdiary
                                        where id = ?;''', (id,))
        return

    def get_rawdiary_status(self, id: int):
        cursor = self.query_with_params('''select is_draft
                                           from rawdiary
                                           where id = ?''', (id, ))
        result = cursor.fetchone()
        status = int(result[0])
        return status

    def get_unextracted_rawdiary(self):
        cursor = self.query('''SELECT id FROM rawdiary where is_extracted = 0''')
        result = cursor.fetchall()
        ids = list([str(x[0]) for x in result])
        return ids
