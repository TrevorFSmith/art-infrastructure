#!/bin/bash

set -e

# Activate the Python virtual environment
source /home/art/.virtualenvs/ai/bin/activate

# Run gunicorn
cd /var/www/art-infrastructure/django/
exec gunicorn wsgi -c gunicorn.py &
