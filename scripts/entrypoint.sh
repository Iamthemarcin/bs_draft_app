#!/bin/sh

echo "Entrypoint is being read correctly"

if [ "$DATABASE" = "postgres" ]
then
    echo "Waiting for postgres..."

    while ! nc -z $SQL_HOST $SQL_PORT; do
      sleep 0.1
    done

    echo "PostgreSQL started"
fi

if [ "$CRON" = "true" ]
then
    echo "Cron has started"
fi


exec "$@"
