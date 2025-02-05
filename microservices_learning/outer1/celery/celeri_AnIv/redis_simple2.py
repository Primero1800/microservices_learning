import json
import os
from dataclasses import asdict

import redis
from outer1.celery.celeri_AnIv import config

redis_params = config.REDIS_PARAMS

class Kolbas:
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            self.__setattr__(key, value)

    def to_json(self):
        dictionary = {key: self.__getattribute__(key) for key in self.__dict__}
        dictionary['_class'] = 'Kolbas'
        return dictionary

    def __repr__(self):
        return f"Kolbas({', '.join(f'{key}={value}' for key, value in self.__dict__.items())})"

    def __str__(self):
        return self.__repr__()


def get__app_name():
    return os.path.basename(__file__).split('.')[0]


def main():
    app_name = get__app_name()
    with redis.Redis(**redis_params) as client:
        client.rpush(app_name, json.dumps({
            'name': 'Ivan',
            'profession': 'durak',
        }))
        client.rpush(app_name, json.dumps('corowa'))

        client.rpush(app_name, json.dumps(['dog', 'cat']))

        client.rpush(app_name, json.dumps([1, '11']))

        client.rpush(app_name, json.dumps(100500))

        kolbas1 = Kolbas(name='Ivan', age=29)
        d = 2
        client.rpush(app_name, json.dumps(kolbas1.to_json()))

        print(client.lrange(app_name, 0, -1))

        while True:
            item = client.lpop(app_name)
            if not item:
                break
            try:
                item = json.loads(item)
            except json.JSONDecodeError:
                item = item.decode()
            if isinstance(item, dict) and '_class' in item:
                item = class_from_dict(item)
            print(item, type(item))


def class_from_dict(data: dict):
    class_name = data.pop('_class')
    class_ = globals().get(class_name)
    if not class_:
        raise ValueError(f"Класс '{class_name}' не найден.")
    return class_(**data)


if __name__ == "__main__":
    main()