#!/bin/bash

cd /opt/echo-fs

./wait_for_redis.sh

echo "Starting echo-scavenger with RedisHost=$ECHO_REDIS_HOST, RedisPort=$ECHO_REDIS_PORT, RedisDB=$ECHO_REDIS_DB"

python -u echo_scavenger.py
