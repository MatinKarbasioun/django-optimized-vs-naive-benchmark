#!/bin/sh

set -e

mkdir -p /app/staticfiles

echo "Applying database migrations..."
python manage.py migrate --no-input

exec "$@"
