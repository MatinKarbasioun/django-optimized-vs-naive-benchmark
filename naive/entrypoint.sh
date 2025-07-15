#!/bin/sh

set -e

echo "Applying database migrations..."
python manage.py migrate --no-input
python manage.py collectstatic --noinput

exec "$@"
