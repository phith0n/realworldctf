#!/bin/sh

BASE_DIR=$(pwd)
./manage.py collectstatic --no-input
./manage.py migrate --no-input

exec uwsgi --socket 0.0.0.0:8000 --module rwctf.wsgi --chdir ${BASE_DIR} --uid nobody --gid nogroup --cheaper-algo spare --cheaper 2 --cheaper-initial 4 --workers 10 --cheaper-step 1
