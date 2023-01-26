run: env/bin/python noted/core/settings/local.py
	./env/bin/python noted/manage.py runserver --settings=core.settings.local

setdb: env/bin/python noted/core/settings/local.py
	./env/bin/python noted/manage.py makemigrate --settings=core.settings.local

shell: env/bin/python noted/core/settings/local.py
	./env/bin/python noted/manage.py shell --settings=core.settings.local