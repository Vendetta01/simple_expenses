#!/bin/bash
python manage.py migrate                  # Apply database migrations
python manage.py collectstatic --noinput  # Collect static files

# Prepare log files and start outputting logs to stdout
touch /data/logs/gunicorn.log
touch /data/logs/access.log
tail -n 0 -f /data/logs/*.log &

# Start Gunicorn processes
echo Starting Gunicorn.
exec gunicorn simple_expenses.wsgi:application \
    --name simple_expenses \
    --bind 0.0.0.0:8000 \
    --workers 2 \
    --log-level=info \
    --log-file=/data/logs/gunicorn.log \
    --access-logfile=/data/logs/access.log \
    "$@"

# TODO: create production ready script with some proxy that serves static files
# exec python manage.py runserver 0.0.0.0:8000