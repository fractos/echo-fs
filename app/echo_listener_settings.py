import os
import distutils.util

DEBUG = bool(distutils.util.strtobool(os.environ.get("DEBUG", default="False")))

NUM_POOL_WORKERS = 5
MESSAGES_PER_FETCH = 10
LOCK_TIMEOUT = 5

CACHE_ROOT = os.environ.get('ECHO_CACHE_ROOT')
REDIS_HOST = os.environ.get('ECHO_REDIS_HOST')
REDIS_PORT = int(os.environ.get('ECHO_REDIS_PORT'))
REDIS_DB = int(os.environ.get('ECHO_REDIS_DB'))
QUEUE_REGION = os.environ.get('ECHO_QUEUE_REGION')
INPUT_QUEUE = os.environ.get('ECHO_INPUT_QUEUE')
ERROR_QUEUE = os.environ.get('ECHO_ERROR_QUEUE')
AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')
