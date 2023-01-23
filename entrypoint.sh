#!/bin/sh
 
sleep 5
cd noted
python manage.py makemigrate
python manage.py collectstatic --noinput
python noted/manage.py compilemessages -l ru
gunicorn core.wsgi:application --bind 172.18.1.3:8000

