import redis
from outer1.celery.celeri_AnIv import config

redis_params = config.REDIS_PARAMS
keys = []



def main():
    with redis.Redis(**redis_params) as client:
        prefix = get_prefix()
        while True:
            print('\nQUIT - escape, SHOW - print values, DELETE - delete entered values, WASTE SHOW - show waste in redis, WASTE DELETE - delete waste in redis...')
            key = input('Input key: ')

            if key == 'QUIT':
                delete_values(client, prefix)
                client.delete(*get_wasted_keys(client, prefix).values())

                break

            elif key == 'SHOW':
                show_values(client, prefix)

            elif key == 'DELETE':
                delete_values(client, prefix)

            elif key == "WASTE SHOW":
                wasted_keys = get_wasted_keys(client, prefix)
                if wasted_keys:
                    print('Waste in Redis from Application: ')
                    for wkey in wasted_keys:
                        print(f"{wkey}: {client.get(wasted_keys[wkey]).decode()},     ** Redis key: {wasted_keys[wkey]}")
                else:
                    print('No waste')


            elif key == 'WASTE DELETE':
                wasted_keys = get_wasted_keys(client, prefix)
                if wasted_keys:
                    print('Waste from application in Redis:')
                    print(*wasted_keys.values())
                    # wkeys = [key for key in wasted_keys.values()]
                    client.delete(*wasted_keys.values())
                    print('Waste deleted')
                else:
                    print('No waste in Redis')

            else:
                value = input('Input value: ')
                result = client.set(prefix+key, value)
                if result:
                    keys.append(key)


def get_wasted_keys(client, prefix):
    return {
        key.decode().split('_')[-1]: key.decode() for key in client.keys(pattern=f'{prefix}*')
        if key.decode().split('_')[-1] not in keys
    }

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
