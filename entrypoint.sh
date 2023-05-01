#!/bin/bash

# Wait for postgres 
while ! nc -z $DATABASE_HOST $DATABASE_PORT; 
  do sleep 0.1;
done

set -e
# Running gunicorn
cd noted
python manage.py migrate --settings=core.settings.production
python manage.py collectstatic --noinput --settings=core.settings.production
gunicorn core.wsgi:application --bind 0.0.0.0:8000

