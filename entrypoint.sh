#!/bin/sh
 
sleep 5
source env/bin/activate
python noted/manage.py makemigrations
python noted/manage.py makemigrations tags
python noted/manage.py makemigrations notes
python noted/manage.py makemigrations user
python noted/manage.py migrate user
python noted/manage.py migrate tags
python noted/manage.py migrate notes
python noted/manage.py migrate
python noted/manage.py runserver 172.18.1.3:8000

