import asyncio
import aioconsole

import redis
from outer1.celery.celeri_AnIv import config

redis_params = config.REDIS_PARAMS
#redis_params = config.RABBITMQ_PARAMS

def problemator():
    with redis.Redis(**redis_params) as client:
        while True:
            problem = input(":::")

            if problem == 'q':
                break

            elif problem == 'a':
                answer = client.rpop('result_strs')
                if answer:
                    answer = answer.decode()
                    print('Solved task: ', answer)

            elif problem == 'aa':
                while True:
                    answer = client.rpop('result_strs')
                    if answer:
                        answer = answer.decode()
                        print('Solved task: ', answer)
                    else:
                        break

            else:
                client.lpush('problems', problem)


problemator()
