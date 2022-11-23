#!/bin/sh
 
sleep 5
cd noted 
python manage.py makemigrations
python manage.py makemigrations tags
python manage.py makemigrations notes
python manage.py makemigrations user
python manage.py makemigrations actions
python manage.py migrate actions
python manage.py migrate user
python manage.py migrate tags
python manage.py migrate notes
python manage.py migrate
python manage.py collectstatic --noinput
gunicorn noted.wsgi:application --bind 172.18.1.3:8000

