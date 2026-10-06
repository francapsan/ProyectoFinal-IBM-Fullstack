#!/bin/sh
set -e

echo "Applying database migrations..."
python manage.py makemigrations dealerships --noinput || true
python manage.py migrate --noinput

echo "Seeding initial root user and car makes/models..."
python manage.py seed_data

echo "Collecting static files..."
python manage.py collectstatic --noinput || true

echo "Starting Django server..."
exec "$@"
