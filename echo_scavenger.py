import echo_scavenger_settings as settings
import os.path
import sys
import redis
import time
import random
import string
import datetime

def main():
	if len(sys.argv) < 3:
		showUsage()
		return
	
	redisHost = sys.argv[1]
	redisPort = int(sys.argv[2])
	redisDB = int(sys.argv[3])
			
	global redisClient
	redisClient = redis.Redis(host=redisHost, port=redisPort, db=redisDB)

	percentageFree = get_free_space(settings.CACHE_ROOT)
	
	console_log("percentage free = %s" % str(round(percentageFree, 2)))
	
	# loop forever
	
	# check disk space
	# if disk space below threshold:
	#   get cardinality of access set
	#   calculate x% of the cardinality
	#   get range from access set
	#   iterate through range:
	#     rename file to '.deleting'
	#     remove from access set
	#     delete file
		
def get_free_space(pathname):
	st = os.statvfs(pathname)
    free = st.f_bavail * st.f_frsize
    total = st.f_blocks * st.f_frsize
    used = st.f_frsize * (st.f_blocks - st.f_bfree)
	if total > 0:
		return 100 - (100 * (float(used) / total))

	return 100

def showUsage():
	print "Usage: echo_scavenger.py <Redis IP> <Redis Port> <Redis DB>"
	print "Example: echo_listener.py 172.17.0.2 6379 0"
	
def console_log(message):
	print('{:%Y%m%d %H:%M:%S} '.format(datetime.datetime.now()) + message)
	
if __name__ == "__main__":
	main()
