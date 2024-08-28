#!/usr/bin/env bash

set -e

chown www-data:www-data /var/log
while ! nc -z $SQL_HOST $SQL_PORT; do
      sleep 0.1
done
python manage.py migrate
python manage.py collectstatic --noinput
python manage.py create_superuser
uwsgi --strict --ini /opt/app/uwsgi/uwsgi.ini
