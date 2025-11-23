#!/bin/sh
set -e

# Render では $PORT が与えられる（デフォルトで 8000 を使う）
export PORT=${PORT:-8000}

# マイグレーション（失敗しても続行しないようにしておく）
echo "Apply migrations..."
python manage.py migrate --noinput

# static を収集（WhiteNoise で配信する前提）
echo "Collect static files..."
python manage.py collectstatic --noinput

# Gunicorn でアプリ起動
echo "Starting Gunicorn on port ${PORT}..."
exec gunicorn portfolio.wsgi:application --bind 0.0.0.0:${PORT} --workers 3 --log-level info
