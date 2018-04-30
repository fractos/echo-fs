import echo_populate_settings as settings
import os.path
import sys
import redis
import time
import string
import datetime

def main():
  global redisClient
  redisClient = redis.Redis(
    host=settings.REDIS_HOST,
    port=settings.REDIS_PORT,
    db=settings.REDIS_DB)

  for path, subdirs, files in os.walk(settings.CACHE_ROOT):
    for filename in files:
      full_path_name = os.path.join(path, filename)
      unix_timestamp = os.path.getmtime(full_path_name)

      access_time = int(unix_timestamp)
      adding_name = full_path_name[len(settings.CACHE_ROOT):]

      console_log("adding %s as %s: %s" %
        (full_path_name, adding_name, str(access_time)))

      redisClient.zadd('access', adding_name, access_time)

def console_log(message):
    print('{:%Y%m%d %H:%M:%S} '.format(datetime.datetime.now()) + message)

if __name__ == "__main__":
    main()
