#!/bin/bash

cd /opt/echo-fs

./wait_for_redis.sh

echo "Starting echo-listener with Redis=$ECHO_REDIS_HOST, RedisPort=$ECHO_REDIS_PORT, RedisDB=$ECHO_REDIS_DB, Region=$ECHO_QUEUE_REGION, InputQueue=$ECHO_INPUT_QUEUE, ErrorQueue=$ECHO_ERROR_QUEUE"

python -u echo_listener.py
