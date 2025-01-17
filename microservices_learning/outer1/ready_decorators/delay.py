import asyncio
from functools import partial


def async_delay(func=None, delay=0):
    if func is None:
        return partial(async_delay, delay=delay)
    async def wrapper(*args, **kwargs):
        await asyncio.sleep(delay)
        return await func(*args, **kwargs)

    return wrapper