from multiprocessing import Pool
import echo_listener_settings as settings
from boto import sqs
from boto.sqs.message import RawMessage
from boto.s3.connection import S3Connection
from boto.s3.key import Key
import json
import os.path


class AgnosticMessage(RawMessage):
    """
    A message might originate from SNS or SQS. If from SNS then it will have a wrapper on it.
    """

    def get_effective_message(self):
        body = json.loads(str(self.get_body()))
        if 'Type' in body and body['Type'] == "Notification":
            return json.loads(body['Message'])
        return body


def main():
    global s3Connection
    s3Connection = S3Connection()

    input_queue = get_input_queue()

    input_queue.set_message_class(AgnosticMessage)

    num_pool_workers = settings.NUM_POOL_WORKERS
    messages_per_fetch = settings.MESSAGES_PER_FETCH

    pool = Pool(num_pool_workers, initargs=())

    while True:
        messages = input_queue.get_messages(num_messages=messages_per_fetch, visibility_timeout=120,
                                            wait_time_seconds=20)
        if len(messages) > 0:
            pool.map(process_message, messages)


def process_message(message):
    message_body = message.get_effective_message()
    if '_type' in message_body and 'message' in message_body and 'params' in message_body:
        if message_body['message'] == "echo::cache-item":
            cache_item(message_body['params'])

    message.delete()


def cache_item(payload):
    # "source": "s3://my-bucket/key"
    # "target": "/my-path/key.maybe-extension-too
    # "bucket": "my-bucket"
    # "key": "key"

    print "received request to cache " + payload['bucket'] + '/' + payload['key'] + ' to ' + payload['target']

    bucket = s3Connection.get_bucket(payload['bucket'])

    k = Key(bucket)
    k.key = payload['key']

    target = settings.CACHE_ROOT + payload['target'].decode('utf-8')

    targetPath = '/'.join(target.split('/')[0:-1])

    if not os.path.isdir(targetPath):
        os.makedirs(targetPath)

    if os.path.exists(target):
        print "already exists in cache"
    else:
        k.get_contents_to_filename(target)
        print "downloaded " + payload['key'] + " from s3"


def get_input_queue():
    conn = sqs.connect_to_region(settings.SQS_REGION)
    queue = conn.get_queue(settings.INPUT_QUEUE)
    return queue


if __name__ == "__main__":
    main()
