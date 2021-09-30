release: python manage.py migrate
web: gunicorn UnordToolsProject.wsgi --log-file -
clock: python clock.py