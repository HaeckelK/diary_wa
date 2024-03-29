# diary_wa 0.6.0

## Introduction
Small scale Flask web app to write diary through form and write to database.

Searched for words and status 200 urls are saved in sqlite database (path specified in config.ini).

## Initial Setup
- Copy config_template.ini to config.ini and add database path included .db extension.
```bash
cp diary/config_template.ini diary/config.ini
```
- Create empty categories file:
```bash
touch data/categories.txt
```
- setup venv
```bash
python -m venv venv
source venv/scripts/activate
pip install -r diary/requirements.txt
pip install -r diary/requirements_dev.txt
```
- run python3 initial_setup.py
```bash
python -c "from diary import initial_setup; initial_setup.main();"
```

- set PORT in launch.sh

## Production
### Launching
On server
```bash
bash launch.sh
```

## Development
### Launching
```bash
export FLASK_APP=app.py
export FLASK_ENV=development
export ARTICLES_API_URL=http://192.168.99.100:5125
cd diary
flask run --port=5008
# or
flask run --port=5008 --host=0.0.0.0
```
Windows
```bash
set FLASK_APP=app.py
set FLASK_ENV=development
set ARTICLES_API_URL=http://192.168.99.100:5125
cd diary
flask run --port=5008
# or
flask run --port=5008 --host=0.0.0.0
```
### Releasing
```bash
bump2version minor --message 'build: {new_version}' --dry-run --verbose
bump2version major
```

### Code checks
From root
```bash
mypy .
coverage run --source . -m pytest && coverage html
flake8 --max-line-length 120
```
