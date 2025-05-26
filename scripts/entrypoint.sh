#!/bin/bash
# Apply database migrations
python manage.py migrate --noinput

# Collect static files
python manage.py collectstatic --noinput

# Start the app server (e.g., using gunicorn)
gunicorn conf.wsgi:application --bind 0.0.0.0:80
