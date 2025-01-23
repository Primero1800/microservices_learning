from celery import Celery
import PIL
from PIL import Image

#app = Celery('image_processor', broker='redis://localhost:6379/0')
app = Celery('image_processor', broker='amqp://guest:guest@localhost:5672//')


@app.task
def resize_image(image_path, output_path, size):
    with Image.open(image_path) as img:
        img.thumbnail(size, Image.LANCZOS)
        img.save(output_path)

@app.task
def crop_image(image_path, output_path, crop_box):
    with Image.open(image_path) as img:
        cropped_img = img.crop(crop_box)
        cropped_img.save(output_path)


@app.task
def stop_celery():
    app.close()


resize_image.apply_async(
    ('1.png', 'resized1.png', (300, 260)),
)


crop_image.apply_async(
    ('resized1.png', 'cropped_resized1.png', (100, 100, 200, 200)),
)


stop_celery.delay()

