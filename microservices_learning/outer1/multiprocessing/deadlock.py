import time
from threading import Thread, Lock

l1 = Lock()
l2 = Lock()


def func1():
    print('func1 started')
    with l1:
        print("func1 in lock1")
        time.sleep(2)
        with l2:
            print('func1 passed in lock2')
            time.sleep(2)
    print('func1 free')


def func2():
    print('func2 started')
    with l2:
        print("func2 in lock2")
        time.sleep(2)
        with l1:
            print('func2 passed in lock1')
            time.sleep(2)
    print('func2 free')


if __name__ == "__main__":

    funcs = [func1, func2]

    ths = [Thread(target=func) for func in funcs]
    [th.start() for th in ths]