run: env/bin/python noted/core/settings/local.py noted/manage.py
	./env/bin/python noted/manage.py runserver --settings=core.settings.local

setdb: env/bin/python noted/core/settings/local.py noted/manage.py
	./env/bin/python noted/manage.py makemigrate --settings=core.settings.local

shell: env/bin/python noted/core/settings/local.py noted/manage.py
	./env/bin/python noted/manage.py shell --settings=core.settings.local

flushdb: env/bin/python noted/core/settings/local.py noted/manage.py
	./env/bin/python noted/manage.py flush --settings=core.settings.local

clear_migrations:
	find noted/ -type d -name migrations -exec rm -v -rf {} +
	

clear_pycache:
	find noted/ -type d -name __pycache__ -exec rm -v -rf {} +

clear: clear_migrations clear_pycache

createsuperuser: env/bin/python noted/core/settings/local.py noted/manage.py
	./env/bin/python noted/manage.py createsuperuser --settings=core.settings.local

test: env/bin/python noted/core/settings/local.py noted/manage.py
	./env/bin/python noted/manage.py test actions common content core tags users --settings=core.settings.test

