#!/bin/bash

. "$(dirname $0)/../tools/script-setup"

rm -f default.sqlite3
python manage.py syncdb --noinput

python manage.py loaddata development_init.json
