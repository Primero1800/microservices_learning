import os
from dotenv import load_dotenv

load_dotenv()


REDIS_PARAMS = {
    'host': os.getenv('REDIS_HOST'),
    'port': os.getenv('REDIS_PORT'),
    'db': os.getenv('REDIS_DB'),
}


RABBITMQ_PARAMS = {
    'host': os.getenv('RABBITMQ_HOST'),
    'port': os.getenv('RABBITMQ_PORT'),
    'user': os.getenv('RABBITMQ_USER'),
    'password': os.getenv('RABBITMQ_PASSWORD'),
    'vhost': os.getenv('RABBITMQ_VHOST'),
}