#!/bin/ash

if [ "$DATABASE" = "postgres" ]
then
    echo "Waiting for postgres..."

    while ! nc -z $SQL_HOST $SQL_PORT; do
      sleep 0.1
    done

    echo "PostgreSQL started"
fi
echo "$1"
if [ $1 = crond ]; then
  python3 manage.py crontab add
  python3 manage.py crontab show
fi
#python3 manage.py flush --no-input
python3 manage.py migrate

exec "$@"