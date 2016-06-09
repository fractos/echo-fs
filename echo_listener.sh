#!/bin/bash

cd /opt/echo-fs

echo "Activating python virtual environment"
source venv/bin/activate

echo "Starting echo-listener with Redis=$1, Region=$2, Queue=$3"

python echo_listener.py $1 $2 $3
