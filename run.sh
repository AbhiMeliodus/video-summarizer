#!/bin/bash
set -e  # Exit on any error

echo "📦 Installing Python dependencies..."
pip install -r requirements.txt --quiet

echo "🗂️ Collecting static files..."
cd videosummarizer
python manage.py collectstatic --noinput

echo "🚀 Starting Gunicorn server..."
gunicorn videosummarizer.wsgi:application \
  --bind 0.0.0.0:8080 \
  --workers 1 \
  --timeout 120 \
  --keep-alive 5 \
  --log-level info
