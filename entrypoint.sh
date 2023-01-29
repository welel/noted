#!/bin/sh
 
sleep 5
cd noted
python manage.py makemigrate --settings=core.settings.prodaction
python manage.py collectstatic --noinput --settings=core.settings.prodaction
gunicorn core.wsgi:application --bind noted-django:8000

