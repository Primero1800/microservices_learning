from datetime import datetime
from functools import wraps, partial


# def timed(func=None, to_time=True):
#     def decorator(func):
#         @wraps(func)
#         def wrapper(*args, **kwargs):
#             if to_time:
#                 start_time = datetime.now()
#                 result = func(*args, **kwargs)
#                 execute_time = datetime.now() - start_time
#                 print(func.__name__, result, execute_time)
#             else:
#                 result = func(*args, **kwargs)
#                 print(func.__name__, result)
#             return result
#         return wrapper
#     if func:
#         return decorator(func)
#     return decorator


def timed(func=None, to_time=True):
    if func is None:
        return partial(timed, to_time=to_time)
    @wraps(func)
    def wrapper(*args, **kwargs):
        if to_time:
            start_time = datetime.now()
            result = func(*args, **kwargs)
            execute_time = datetime.now() - start_time
            print(func.__name__, func.__class__, func.__module__, result, execute_time)
        else:
            result = func(*args, **kwargs)
            print(func.__name__, result)
        return result
    return wrapper


class TestString:
    def __init__(self, value):
        self.value = value

    @timed
    def plus(self, b):
        return self.value + b

    @timed
    def iplus(self, b):
        self.value += b
        return self.value

    @timed
    def join(self, b):
        return ''.join((self.value, b))

    @timed(to_time=False)
    def neutral(self, b):
        return self.value*30 + 30*b


if __name__ == "__main__":

    a = TestString('init')
    b = 'tini'
    a.neutral(b)

    print()


    a = TestString('abbracadabra')
    b = 'solenyiogurets'
    a.iplus(b)

    a = TestString('abbracadabra')
    b = 'solenyiogurets'
    a.plus(b)

    a = TestString('abbracadabra')
    b = 'solenyiogurets'
    a.join(b)


