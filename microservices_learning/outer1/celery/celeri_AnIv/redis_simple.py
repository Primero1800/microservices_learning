import redis
from outer1.celery.celeri_AnIv import config

redis_params = config.REDIS_PARAMS
keys = []


def main():
    with redis.Redis(**redis_params) as client:
        while True:
            print('\nQUIT - escape, SHOW - print values, DELETE - delete entered values')
            key = input('Input key: ')
            if key == 'QUIT':
                break
            elif key == 'SHOW':
                show_values(client)
            elif key == 'DELETE':
                delete_values(client)
            else:
                value = input('Input value: ')
                result = client.set(key, value)
                if result:
                    keys.append(key)


def show_values(client: redis.Redis):
    for key in keys:
        print(key, ': ', client.get(key).decode())


def delete_values(client: redis.Redis):
    for key in keys:
        client.delete(key)
    print(f"KEYS {keys} deleted")
    keys.clear()


if __name__ == "__main__":
    main()
