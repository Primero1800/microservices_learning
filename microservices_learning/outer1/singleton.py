from functools import wraps

def singleton2(cls):
    instances = {}
    @wraps(cls)
    def wrapper(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]
    return wrapper


class Singleton:
    def __init__(self, cls):
        self._cls = cls
        self._instance = None

    def __call__(self, *args, **kwargs):
        if self._instance is None:
            self._instance = self._cls(*args, **kwargs)
        return self._instance


@Singleton
class Bomber:
    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs
        self.id = id(self)


@Singleton
class Bomz:
    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs
        self.id = id(self)


if __name__ == "__main__":
    b1 = Bomber(1, bazuka=4)
    print(b1, b1.args, b1.kwargs, b1.id)

    b2 = Bomber(7, 8, ruka='r')
    print(b2, b2.args, b2.kwargs, b2.id)

    b3 = Bomz('r', ruka='eeer')
    print(b3, b3.args, b3.kwargs, b3.id)

    b4 = Bomz('rrrr', ruka='eerrrer')
    print(b4, b4.args, b4.kwargs, b4.id)

    print(Singleton)
