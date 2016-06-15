#!/bin/bash

cd /opt/echo-fs

echo "Activating python virtual environment"
source venv/bin/activate

echo "Starting echo-scavenger with RedisHost=$1, RedisPort=$2, RedisDB=$3"

python echo_scavenger.py $1 $2 $3
