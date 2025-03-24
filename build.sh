#!/bin/bash
# exit on error
set -o errexit

# Install dependencies
pip install -r requirements.txt

# Set environment variables
export PYTHONPATH=/opt/render/project/src/app
export DJANGO_SETTINGS_MODULE=settings

# Collect static files
cd /opt/render/project/src/app
python manage.py collectstatic --noinput

# Apply database migrations
python manage.py migrate