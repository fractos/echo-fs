import os
import distutils.util

DEBUG = bool(distutils.util.strtobool(os.environ.get("DEBUG", default="False")))

REDIS_HOST = os.environ.get('ECHO_REDIS_HOST')
REDIS_PORT = int(os.environ.get('ECHO_REDIS_PORT'))
REDIS_DB = int(os.environ.get('ECHO_REDIS_DB'))
CACHE_ROOT = os.environ.get('ECHO_CACHE_ROOT')

CACHE_FREE = int(os.environ.get('ECHO_SCAVENGER_CACHE_THRESHOLD', default="50"))
CHUNK_SIZE = int(os.environ.get('ECHO_SCAVENGER_CHUNK_SIZE', default="10"))

NUM_POOL_WORKERS = 5
MESSAGES_PER_FETCH = 10
LOCK_TIMEOUT = 5

QUEUE_REGION = os.environ.get('ECHO_QUEUE_REGION')
INPUT_QUEUE = os.environ.get('ECHO_INPUT_QUEUE')
ERROR_QUEUE = os.environ.get('ECHO_ERROR_QUEUE')
SCAVENGER_SLEEP_SECONDS = int(os.environ.get('ECHO_SCAVENGER_SLEEP_SECONDS', default="30"))

POPULATE_LOOP = bool(distutils.util.strtobool(os.environ.get("ECHO_POPULATE_LOOP", default="False")))
POPULATE_SLEEP_SECONDS = int(os.environ.get("ECHO_POPULATE_SLEEP_SECONDS", default="300"))
