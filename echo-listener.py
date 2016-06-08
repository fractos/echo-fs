from multiprocessing import Pool
import echo_listener_settings as settings
from boto import sqs
from boto.sqs.message import RawMessage
from boto.s3.connection import S3Connection
import json
import os.path



def main():
	input_queue = get_input_queue()

	num_pool_workers = settings.NUM_POOL_WORKERS
	messages_per_fetch = settings.MESSAGES_PER_FETCH

	pool = Pool(num_pool_workers, initializer=init_pool, initargs=())

	try:
		while True:
			messages = input_queue.get_messages(num_messages=messages_per_fetch, visibility_timeout=120, wait_time_seconds=20)
			if len(messages) > 0:
				pool.map(process_message, messages)
	except:
		print "Error getting messages"

def process_message(message):
	try:
		message_body = json.loads(str(message.get_body()))

		if '_type' in message_body and 'message' in message_body and 'params' in message_body:
			if message_body['message'] == "echo::cache-item":
				cache_item(message_body['params'])

	except Exception as e:
		print e

	message.delete()

def cache_item(payload):
	# "source": "s3://my-bucket/key"
	# "target": "/my-path/key.maybe-extension-too
	# "bucket": "my-bucket"
	# "key": "key"
	




def init_pool():
	global output_queue
	output_queue = get_output_queue()

def get_input_queue():
	conn = sqs.connect_to_region(settings.SQS_REGION)
	queue = conn.get_queue(settings.INPUT_QUEUE)
	return queue

if __name__ == "__main__":
	aws_connection = S3Connection()
	main()
