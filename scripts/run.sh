#!/bin/sh

set -e

ls -la /vol/
ls -la /vol/web

whoami

python3 manage.py wait_for_db
python3 manage.py collectstatic --noinput
python3 manage.py migrate

uwsgi --socket :9000 --workers 4 --master --enable-threads --module power_draft.wsgi