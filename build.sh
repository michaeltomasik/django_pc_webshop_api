#!/bin/bash
# exit on error
set -o errexit

# Install dependencies
pip install -r requirements.txt

# Set environment variables
export PYTHONPATH=$PYTHONPATH:/opt/render/project/src
export DJANGO_SETTINGS_MODULE=app.app.settings

# Collect static files
python app/manage.py collectstatic --noinput

# Apply database migrations
python app/manage.py migrate