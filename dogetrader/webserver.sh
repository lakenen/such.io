#!/bin/bash

. "$(dirname $0)/../tools/script-setup"

python manage.py runserver 0.0.0.0:8000
