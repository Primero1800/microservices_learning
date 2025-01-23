from celery import Celery
from PIL import Image


app = Celery('cel_processor', broker='redis://localhost:6379/0')

@app.task
def reporter(img_path):
    try:
        with open(img_path, 'rb') as img, open('reporter.txt', 'w') as file:
            for line in img.readlines():
                file.write(str(line))
    except (UnboundLocalError, FileNotFoundError) as error:
        with open('reporter.txt', 'wb') as file:
            file.write(f"{img_path}: {error}".encode())


reporter.apply_async(args=('11.png', ), )

