from multiprocessing import Pool
import echo_listener_settings as settings
from boto import sqs
from boto.sqs.message import RawMessage
from boto.s3.connection import S3Connection
from boto.s3.key import Key
import json
import os.path
import sys
import redis
import time
import random
import string
import datetime

class AgnosticMessage(RawMessage):
	"""
	A message might originate from SNS or SQS. If from SNS then it will have a wrapper on it.
	"""
	
	def get_effective_message(self):
		b = json.loads(str(self.get_body()))
		if 'Type' in b and b['Type'] == "Notification":
			return json.loads(b['Message'])
		return b

def main():
	if len(sys.argv) < 5:
		showUsage()
		return
	
	redisHost = sys.argv[1]
	redisPort = int(sys.argv[2])
	redisDB = int(sys.argv[3])
			
	input_queue = get_input_queue(sys.argv[4], sys.argv[5])

	input_queue.set_message_class(AgnosticMessage)
	
	num_pool_workers = settings.NUM_POOL_WORKERS
	messages_per_fetch = settings.MESSAGES_PER_FETCH

	pool = Pool(num_pool_workers, initializer=workerSetup, initargs=(redisHost, redisPort, redisDB))

	while True:
			messages = input_queue.get_messages(num_messages=messages_per_fetch, visibility_timeout=120, wait_time_seconds=20)
			if len(messages) > 0:
					pool.map(process_message, messages)

def workerSetup(redisHost, redisPort, redisDB):
	global s3Connection
	s3Connection = S3Connection()
	
	global redisClient
	redisClient = redis.Redis(host=redisHost, port=redisPort, db=redisDB)
						
def showUsage():
	print "Usage: echo_listener.py <Redis IP> <Redis Port> <Redis DB> <AWS region> <AWS queue name>"
	print "Example: echo_listener.py 172.17.0.2 6379 0 eu-west-1 echo-eu-west-1a"

def process_message(message):
	message_body = message.get_effective_message()
	if '_type' in message_body and 'message' in message_body and 'params' in message_body:
		if message_body['message'] == "echo::cache-item":
			cache_item(message_body['params'])
		elif message_body['message'] == "echo::item-access":
			item_access(message_body['params'])

	message.delete()

def item_access(payload):
	console_log("item_access: " + payload['target'])
	
	target = settings.CACHE_ROOT + payload['target'].decode('utf-8')
	
	record_access(target)
			
def cache_item(payload):
	# "source": "s3://my-bucket/key"
	# "target": "/my-path/key.maybe-extension-too
	# "bucket": "my-bucket"
	# "key": "key"
	
	console_log("cache_item: s3://" + payload['bucket'] + '/' + payload['key'] + ' -> ' + payload['target'])

	target = settings.CACHE_ROOT + payload['target'].decode('utf-8')

	targetPath = '/'.join(target.split('/')[0:-1])	

	try:
		if not os.path.isdir(targetPath):
			os.makedirs(targetPath)
	except:
		pass

	record_access(target)
		
	if os.path.exists(target):		
		console_log("already exists in cache")
	else:
		console_log("synchronisation lock")
		timeout_start = time.time()
		timeout = settings.LOCK_TIMEOUT
		
		# if the flag exists, then loop until timeout for the flag to disappear
		if redisClient.exists(payload['target']):
			while time.time() < timeout_start + timeout:
				if redisClient.exists(payload['target']):
					# currently an operation happening for this file
					time.sleep(0.01)
				else:
					timeout_occurred = false
					break
					
			if timeout_occurred:
				print "lock timeout"
				return
		
		if not os.path.exists(target):
			redisClient.set(payload['target'], payload['target'])
	
			bucket = s3Connection.get_bucket(payload['bucket'])

			k = Key(bucket)
			k.key = payload['key']

			try:
				k.get_contents_to_filename(target)
				console_log("downloaded " + payload['key'] + " from s3")
			except Exception as e:
				console_log("problem while trying to download file " + k.key + ": " + e)
				pass
				
			redisClient.delete(payload['target'])
	
def record_access(item):
	#print "record_access for " + item
	accessTime = int(time.time())
	redisClient.zadd('access', item, accessTime)
	
def get_input_queue(region, queue):
	conn = sqs.connect_to_region(region)
	return conn.get_queue(queue)

def console_log(message):
	print('{:%Y%m%d %H:%M:%S} %s'.format(datetime.datetime.now(), message))
	
if __name__ == "__main__":
	main()
