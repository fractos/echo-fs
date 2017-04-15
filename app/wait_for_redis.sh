#!/bin/bash

# wait for db to come up before starting tests, as shown in https://github.com/docker/compose/issues/374#issuecomment-126312313
# uses bash instead of netcat, because netcat is less likely to be installed
# strategy from http://superuser.com/a/806331/98716
set -e

echoerr() { echo "$@" 1>&2; }

echoerr wait: waiting for $ECHO_REDIS_HOST:$ECHO_REDIS_PORT

timeout 15 bash <<EOT
while ! (echo > /dev/tcp/$ECHO_REDIS_HOST/$ECHO_REDIS_PORT) >/dev/null 2>&1;
    do sleep 1;
done;
EOT
RESULT=$?

if [ $RESULT -eq 0 ]; then
  sleep 1
  echoerr wait: done
else
  echoerr wait: timeout out after 15 seconds waiting for $ECHO_REDIS_HOST:$ECHO_REDIS_PORT
fi

