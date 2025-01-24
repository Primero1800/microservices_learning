from asyncio.log import logger
from functools import wraps

from celery import Celery
from PIL import Image


app1 = Celery('image_processor', broker='amqp://guest:guest@localhost:5672//')
#app2 = Celery('image_processor2', broker='redis://localhost:6379/0')

app1.conf.broker_connection_always_reconnect = True
app1.conf.broker_connection_retry_on_startup = True



def retry(timeout=10):
    def decorator(func):
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as ex:
                return self.retry(countdown=timeout, max_retries=15)
        return wrapper
    return decorator


@app1.task(bind=True)
@retry(timeout=2)
def resize_image(image_path, output_path, size):
    with Image.open(image_path) as img:
        img.thumbnail(size, Image.LANCZOS)
        img.save(output_path)


@app1.task(bind=True)
@retry(timeout=5)
def crop_image(image_path, output_path, crop_box):
    with Image.open(image_path) as img:
        cropped_img = img.crop(crop_box)
        cropped_img.save(output_path)



resize_image.apply_async(
    ('1.png', 'resized1.png', (300, 260)),
)


crop_image.apply_async(
    ('resized1.png', 'cropped_resized1.png', (100, 100, 200, 200)),
)

