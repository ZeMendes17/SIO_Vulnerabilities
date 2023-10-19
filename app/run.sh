#!/bin/bash

if [ -d "../instance" ]; then
  rm -r "../instance"
fi

export FLASK_APP=__init__.py
export FLASK_DEBUG=1

flask run &

sleep 2

curl "http://127.0.0.1:5000/generate/database"

read -p "Press Enter to close Flask and continue"

kill %1
