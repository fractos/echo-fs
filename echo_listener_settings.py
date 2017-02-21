NUM_POOL_WORKERS = 5
MESSAGES_PER_FETCH = 10
CACHE_ROOT = '/exports/efs'
LOCK_TIMEOUT = 5

try:
	from secrets import *
except ImportError:
	pass
