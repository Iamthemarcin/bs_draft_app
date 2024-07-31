#!/bin/sh

# Navigate to the Django project directory
now="$(date +"%T")"
echo "Starting the battles scan at $now"
# Run the Django management command
python3 manage.py update_db