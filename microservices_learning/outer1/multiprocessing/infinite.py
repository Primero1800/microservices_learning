import time
from random import random
from threading import Thread, Lock


class CounterLock:
    def __init__(self, *args, **kwargs):
        self.lock = Lock()
        self.counter = 0

    def increase(self):
        self.counter += 1
        return self.counter


cl = CounterLock()


def func1():
    with cl.lock:
        print(f'{cl.increase()}. func1 started')
    time.sleep(random())
    func2()
    print('func1 free')


def func2():
    with cl.lock:
        print(f'{cl.increase()}. func2 started')
    time.sleep(random())
    func1()
    print('func2 free')


if __name__ == "__main__":

    funcs = [func1, func2]

    ths = [Thread(target=func) for func in funcs]
    [th.start() for th in ths]