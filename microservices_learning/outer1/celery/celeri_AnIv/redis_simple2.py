import json
import os

import redis
from outer1.celery.celeri_AnIv import config

redis_params = config.REDIS_PARAMS

def get__app_name():
    return os.path.basename(__file__).split('.')[0]

def main():
    app_name = get__app_name()
    with redis.Redis(**redis_params) as client:
        client.rpush(app_name, json.dumps({
            'name': 'Ivan',
            'profession': 'durak',
        }))
        client.rpush(app_name, 'corowa')

        print(client.lrange(app_name, 0, -1))

        while True:
            item = client.lpop(app_name)
            if not item:
                break
            try:
                item = json.loads(item)
            except json.JSONDecodeError:
                item = item.decode()
            print(item, type(item))




if __name__ == "__main__":
    main()