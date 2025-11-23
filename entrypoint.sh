#!/bin/sh
set -e

# Render が提供する PORT 環境変数を使用
export PORT=${PORT:-8000}

echo "Apply migrations..."
python manage.py migrate --noinput

echo "Collect static files..."
python manage.py collectstatic --noinput

echo "Starting Gunicorn on port ${PORT}..."
exec gunicorn portfolio.wsgi:application --bind 0.0.0.0:${PORT} --workers 3 --log-level info
