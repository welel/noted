#!/bin/bash

# Makes `.po` translation files.
# Make sure that you have a symlink to the root Django project directory before the execution.  
# Execute from the current directory.

cd ../../../frontend/
django-admin makemessages -l ru --all --ignore=env --symlinks
django-admin makemessages -l ru -d djangojs --all --ignore=env --symlinks