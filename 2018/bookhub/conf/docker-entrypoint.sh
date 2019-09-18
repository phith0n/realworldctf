#!/bin/sh
set -e

if [ ! -e /data/db.sqlite3 ]; then
    flask db upgrade
    chown nobody:nogroup /data/db.sqlite3
fi

exec "$@"