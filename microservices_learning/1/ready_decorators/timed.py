from datetime import datetime

def timed(func):
    def wrapper(*args, **kwargs):
        start_time = datetime.now()
        result = func(*args, **kwargs)
        print(f"{func.__name__} worked: {datetime.now()-start_time}")
        return result
    return wrapper


def async_timed(func):
    async def wrapper(*args, **kwargs):
        start_time = datetime.now()
        result = await func(*args, **kwargs)
        print(f"{func.__name__} worked: {datetime.now()-start_time}")
        return result
    return wrapper
