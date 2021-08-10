import configparser
import sys

from diary.diarydatabase import DiaryDatabase, BookNotesDatabase


def main():
    config = configparser.ConfigParser()
    config.read('diary/config.ini')
    filename = config['DATABASE']['path']
    print('initial setup')
    print('creating database', filename)
    if filename == '':
        print('Database path must specifiy .db file')
        sys.exit()
    for base in (DiaryDatabase, BookNotesDatabase):
        db = base(filename)
        db.initial_setup()
    print('created', filename)
    return


if __name__ == '__main__':
    main()
