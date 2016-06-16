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
		
	while True:
		percentage_free = get_free_space(settings.CACHE_ROOT)
		
		percentage_free = 4.5
		
		console_log("percentage free = %s" % str(round(percentage_free, 2)))
		
		if percentage_free < settings.CACHE_FREE:
			
			console_log("disk space free is below threshold (" + str(settings.CACHE_FREE) + ")")
			
			cardinality = get_access_set_cardinality()
			
			console_log("cardinality= " + str(cardinality))
			
			if cardinality > 0:
				
				chunk_length = (cardinality / 100) * settings.CHUNK_SIZE
				
				if chunk_length < 1:
					chunk_length = 1
					
				chunk = get_access_set_range(chunk_length)
				
				for item in chunk:
					
					target = settings.CACHE_ROOT + item
					
					console_log('deleting: ' + target)
					
					remove_from_access_set(item)
					
					#os.rename(target, target + '.deleting')
					
					#os.remove(target + '.deleting')

def remove_from_access_set(target):

	console_log('removing ' + target + ' from access set')
	
	#redisClient.zrem("access", target)

def get_access_set_range(chunk_length):

	return redisClient.zrange("access", 0, chunk_length)

def get_access_set_cardinality():
	
	return redisClient.zcard("access")
		
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
