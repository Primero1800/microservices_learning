import time
from threading import Thread

import redis
from outer1.celery.celeri_AnIv import config

redis_params = config.REDIS_PARAMS
CHANNEL = 'channel'

def publisher():
    with redis.Redis(**redis_params) as client:
        while True:
            message = input('input message to send: ')
            kwargs = {
                'position': 'bad',
                'count': 1
            }
            client.publish(CHANNEL, message=message, **kwargs)

            if message == 'QUIT':
                break


def subscriber():

    with redis.Redis(**redis_params) as client:
        pubsub = client.pubsub()
        pubsub.subscribe(CHANNEL)

        while True:
             time.sleep(10)
             for message in pubsub.listen():
                print(f'\nGOT!!! from {message['channel'].decode()} got {message['data']}')

                if message == 'QUIT':
                    return



if __name__ == "__main__":

    funcs = [publisher, subscriber]
    ths = [Thread(target=func) for func in funcs]
    [th.start() for th in ths]
