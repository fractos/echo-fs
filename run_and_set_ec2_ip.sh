#!/bin/sh

export ECHO_REDIS_HOST=$(curl http://169.254.169.254/latest/meta-data/local-ipv4 2> /dev/null)

$@
