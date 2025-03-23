#!/bin/sh

if [ "$DATABASE" = "nyc" ]
then
    echo "Waiting for postGIS..."

    while ! nc -z $SQL_HOST $SQL_PORT; do
      sleep 0.1
    done

    echo "PostGIS started"
fi


exec "$@"
