#!/bin/bash

rm db.sqlite3
. venv/bin/activate
python manage.py makemigrations
python manage.py migrate
python execute_inserts.py
