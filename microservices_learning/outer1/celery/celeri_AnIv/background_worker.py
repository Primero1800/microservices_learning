import time

import redis
from outer1.celery.celeri_AnIv import config
redis_params = config.REDIS_PARAMS
#redis_params = config.RABBITMQ_PARAMS

with redis.Redis(**redis_params) as client:
    while True:
        problem = client.brpop('problems')[1].decode() # prpop -> (b'problems', b'2+2')[1]
        try:
            result = eval(problem)
        except Exception as error:
            result = str(f"Error: {error}")

        result_str = f"{problem}={result}"
        client.lpush('result_strs', result_str)

        print(result_str)

        time.sleep(1)
