#!/bin/sh
set -e

if [ "$APP_DEBUG" = "true" ]; then
    exec python manage.py runserver 0.0.0.0:8000
else
    exec gunicorn instory.wsgi:application --bind 0.0.0.0:8000 --workers $GUNICORN_WORKERS
fi
