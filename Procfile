release: python manage.py migrate
web: gunicorn UnordToolsProject.wsgi --log-file -
clock: python asset_app/clock.py