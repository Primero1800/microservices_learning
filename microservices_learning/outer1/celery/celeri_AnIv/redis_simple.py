import redis
from outer1.celery.celeri_AnIv import config

redis_params = config.REDIS_PARAMS
keys = []



def main():
    with redis.Redis(**redis_params) as client:
        prefix = get_prefix()
        d = 2
        while True:
            print('\nQUIT - escape, SHOW - print values, DELETE - delete entered values, WASTE - show waste in redis')
            key = input('Input key: ')
            if key == 'QUIT':
                delete_values(client, prefix)
                break
            elif key == 'SHOW':
                show_values(client, prefix)
            elif key == 'DELETE':
                delete_values(client, prefix)
            elif key == 'WASTE':
                wasted_keys = client.keys(pattern=f'{prefix}*')
                if wasted_keys:
                    print('Waste from application in Redis:')
                    [print(key.decode()) for key in wasted_keys]
                    client.delete(' '.join(key.decode() for key in wasted_keys))
                    keys.clear()
                    print('Waste and keys deleted')
                else:
                    print('No waste in Redis')

            else:
                value = input('Input value: ')
                result = client.set(prefix+key, value)
                if result:
                    keys.append(key)


def get_prefix():
    return '_'.join(
        [
            '_',
            __package__ if __package__ else '',
            __file__ if __file__ else '',
            __name__
        ]
    )

def show_values(client: redis.Redis, prefix: str = ''):
    if keys:
        for key in keys:
            print(key, ': ', client.get(prefix+key).decode())
    else:
        print('No keys')


def delete_values(client: redis.Redis, prefix: str = ''):
    for key in keys:
        client.delete(prefix+key)
    print(f"KEYS {keys} deleted")
    keys.clear()


if __name__ == "__main__":
    main()
