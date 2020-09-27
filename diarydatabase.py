"""
"""
from typing import Optional, Dict

from database import Database, Results


class DiaryDatabase(Database):
    schema = '''CREATE TABLE IF NOT EXISTS rawinput
                (id INTEGER PRIMARY KEY,
                category TEXT,
                rawtext TEXT,
                date INT,
                processed INT,
                date_added INT);
            '''

    def add_raw_diary_entry(self, category: str, rawtext: str, date: int, processed: int, date_added: Optional[int] = None) -> int:
        date_added, _ = self._dates(date_added, date_added)
        params = (category, rawtext, date, processed, date_added)
        new_id = self.insert('''INSERT INTO rawinput(category, rawtext, date, processed, date_added)
                                VALUES(?,?,?,?,?)''', params)
        return new_id

    #def get_word_all(self):
     #   cursor = self.query('''SELECT * FROM word''')
      #  return Results(cursor).fetchall_dict_factory()
