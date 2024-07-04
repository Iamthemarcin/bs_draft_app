#!/bin/ash

if [ "$DATABASE" = "postgres" ]
then
    echo "Waiting for postgres..."

    while ! nc -z $SQL_HOST $SQL_PORT; do
      sleep 0.1
    done

    echo "PostgreSQL started"
fi

if [ $1 = crond ]; then
  python3 manage.py crontab add
fi

#python3 manage.py flush --no-input 

exec "$@"