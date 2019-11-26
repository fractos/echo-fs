#!/bin/sh

export ECHO_REDIS_HOST=$(curl http://169.254.169.254/latest/meta-data/local-ipv4 2> /dev/null)

echo "ECHO_REDIS_HOST set to $ECHO_REDIS_HOST"

cd /opt/echo-fs

python3 -u echo_populate.py
