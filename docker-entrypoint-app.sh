#!/usr/bin/env bash

# Wait for Postgres to be ready
echo "- Waiting for Postgres..."

until pg_isready -h "$POSTGRES_HOST" -p "$POSTGRES_PORT" -U "$POSTGRES_USER"; do
  echo "Postgres is unavailable - sleeping"
  sleep 1
done

echo "- Postgres is up - continuing..."

# Run migrations
echo "- Running python manage.py migrate"
python manage.py migrate

echo "- Starting Gunicorn server..."
exec gunicorn config.wsgi:application --bind 0.0.0.0:8000