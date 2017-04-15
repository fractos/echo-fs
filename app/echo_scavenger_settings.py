import os

REDIS_HOST = os.environ.get('ECHO_REDIS_HOST')
REDIS_PORT = int(os.environ.get('ECHO_REDIS_PORT'))
REDIS_DB = int(os.environ.get('ECHO_REDIS_DB'))
CACHE_ROOT = os.environ.get('ECHO_CACHE_ROOT')
CACHE_FREE = int(os.environ.get('ECHO_SCAVENGER_CACHE_THRESHOLD'))
CHUNK_SIZE = int(os.environ.get('ECHO_SCAVENGER_CHUNK_SIZE'))
SLEEP_SECONDS = int(os.environ.get('ECHO_SCAVENGER_SLEEP_SECONDS'))
