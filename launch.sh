#!/bin/bash
PORT=5008
kill $(lsof -t -i:$PORT)
cd diary
export FLASK_APP=app.py
flask run --port=$PORT --host=0.0.0.0