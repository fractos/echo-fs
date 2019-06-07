import echo_scavenger_settings as settings
import os
import sys
import redis
import time
import random
import string
import datetime
import signal
import logging
from logzero import logger
import logzero

requested_to_quit = False


def main():
    logger.info("starting")

    setup_signal_handling()

    global redisClient
    redisClient = redis.Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=settings.REDIS_DB)

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

    count = 0

    while lifecycle_continues():
        try:
            percentage_free = get_free_space(settings.CACHE_ROOT)
            logger.info("percentage free = %s" % str(round(percentage_free, 2)))

            if percentage_free < settings.CACHE_FREE:
                logger.info("disk space free is below threshold (" + str(settings.CACHE_FREE) + ")")
                cardinality = get_access_set_cardinality()
                logger.info("number of items in access set =  " + str(cardinality) + ", chunk size = " + str(settings.CHUNK_SIZE) + "%")

                if cardinality > 0:
                    chunk_length = (cardinality / 100) * settings.CHUNK_SIZE
                    if chunk_length < 1:
                        chunk_length = 1
                    logger.info(f"chunk length = {chunk_length}")
                    chunk = get_access_set_range(chunk_length)
                    count = 0

                    for item in chunk:
                        target = settings.CACHE_ROOT + item
                        logger.info(f"deleting: {target}")
                        remove_from_access_set(item)

                        try:
                            os.rename(target, f"{target}.deleting")
                            os.remove(f"{target}.deleting")
                            count = count + 1
                        except Exception as e:
                            logger.info(f"hit problem during rename or delete of {target}: {e}")
                            pass

                    logger.info("removed " + str(count) + " items")
        except Exception as e:
            logger.error("hit problem during operation: " + str(e))
            pass

        logger.info(f"sleeping for {settings.SLEEP_SECONDS} second(s)")
        time.sleep(int(settings.SLEEP_SECONDS))


def lifecycle_continues():
    return not requested_to_quit


def signal_handler(signum, frame):
    logger.info("Caught signal %s" % signum)
    global requested_to_quit
    requested_to_quit = True


def setup_signal_handling():
    logger.info("setting up signal handling")
    signal.signal(signal.SIGTERM, signal_handler)
    signal.signal(signal.SIGINT, signal_handler)


def remove_from_access_set(target):
    logger.info(f"removing {target} from access set")
    redisClient.zrem("access", target)


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


if __name__ == "__main__":
    main()
