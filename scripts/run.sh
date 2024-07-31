#!/bin/sh

if [ "$DJANGO" = "true" ]; then
    echo "Ur the king of djangle"
    set -e

    ls -la /vol/
    ls -la /vol/web

    python3 manage.py wait_for_db
    python3 manage.py collectstatic --noinput
    python3 manage.py migrate

    echo "hello from the uwsgi side"

    uwsgi --socket :9000 --workers 3 --master --enable-threads --module power_draft.wsgi
fi
