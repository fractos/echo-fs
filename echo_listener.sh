#!/bin/bash

cd /opt/echo-fs

echo "Activating python virtual environment"
source venv/bin/activate

echo "Starting echo-listener with Redis=$1, RedisPort=$2, RedisDB=$3, Region=$4, InputQueue=$5, ErrorQueue=$6"

python echo_listener.py $1 $2 $3 $4 $5 $6
