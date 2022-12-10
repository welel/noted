#!/bin/sh
 
sleep 5
cd noted 
python manage.py makemigrations users
python manage.py makemigrations content
python manage.py migrate
python manage.py collectstatic --noinput
gunicorn noted.wsgi:application --bind 172.18.1.3:8000

