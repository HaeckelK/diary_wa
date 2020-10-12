import configparser
import sys

from diary.diarydatabase import DiaryDatabase


def main():
    config = configparser.ConfigParser()
    config.read('config.ini')
    filename = config['DATABASE']['path']
    print('initial setup')
    print('creating database', filename)
    if filename == '':
        print('Database path must specifiy .db file')
        sys.exit()
    db = DiaryDatabase(filename)
    db.initial_setup()
    print('created', filename)
    return


if __name__ == '__main__':
    main()
