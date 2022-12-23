#!/bin/bash
cd ../../../frontend/
django-admin makemessages -l ru --all --ignore=env --symlinks
django-admin makemessages -l ru -d djangojs --all --ignore=env --symlinks