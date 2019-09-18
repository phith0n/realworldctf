#!/usr/bin/env bash

wait-for-it 127.0.0.1:6800 -- echo "scrapyd is up"
if [[ $(curl -s http://127.0.0.1:6800/listprojects.json | grep "webpage") == "" ]]; then
    cd /usr/src/webpage
    scrapyd-deploy webpage -p webpage_1o24
fi

cd /usr/src/web
gunicorn app:app --chdir=/usr/src/web -w 4 -k gevent -u nobody -g nogroup -b 0.0.0.0:8001
