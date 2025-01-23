import time

from billiard.exceptions import SoftTimeLimitExceeded, TimeLimitExceeded
from celery import Celery

app = Celery('waiter', broker='redis://localhost:6379/0')

@app.task()
def generate_report(*args, **kwargs):
    error = None
    try:
        time.sleep(7 * 1)
    except SoftTimeLimitExceeded as soft_error:
        print(f"Soft time limit exception * {soft_error}")
        error = soft_error
        time.sleep(7 * 2)
    return error


@app.task()
def long_report(*args, **kwargs):
    time.sleep(1)
    return 200


soft_time_limit = 5 * 1
hard_time_limit = 5 * 2
result = generate_report.apply_async(args=['1', '2'], soft_time_limit=soft_time_limit, time_limit=hard_time_limit)
result2 = long_report.apply_async(args=(), countdown=3600)
print(result)