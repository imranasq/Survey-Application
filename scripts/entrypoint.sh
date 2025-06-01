#!/bin/bash

# Wait for PostgreSQL to be ready
echo "Waiting for postgres..."
while ! nc -z survey_db 5432; do
  sleep 0.1
done
echo "PostgreSQL started"

# Apply database migrations
python manage.py migrate --noinput

# Collect static files
python manage.py collectstatic --noinput

# Start the app server
gunicorn conf.wsgi:application --bind 0.0.0.0:8000
