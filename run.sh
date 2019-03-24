#!/bin/sh
export LC_ALL=C.UTF-8
export LANG=C.UTF-8
export FLASK_APP=auto-water
export FLASK_ENV=development
./bin/flask run --host=0.0.0.0
