#!/bin/bash
# exit on error
set -o errexit

# Install dependencies
pip install -r requirements.txt

# Set environment variables
export PYTHONPATH=/opt/render/project/src
export DJANGO_SETTINGS_MODULE=app.app.settings

# Change to the app directory
cd app

# Collect static files
python manage.py collectstatic --noinput

# Apply database migrations
python manage.py migrate