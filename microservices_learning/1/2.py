import time
from concurrent.futures import ThreadPoolExecutor
from itertools import cycle
from random import randint

def wait_on(n, rud):
    b = rud
    time.sleep(randint(1, 2))
    print(n, ' ********** ', n)  # b никогда не завершится, потому что ждет a.
    return n


def wait_on_b2(n, rud):
    b = rud
    time.sleep(randint(2, 4))
    print(n**2, ' ********** ', n)  # b никогда не завершится, потому что ждет a.
    return n**2


def wait_on_b3(n, rud):
    b = rud
    time.sleep(randint(3, 4))
    print(n**3, ' ********** ', n)  # a никогда не завершится, потому что ждет b.
    return n**3

if __name__ == "__main__":

    funcs = [wait_on, wait_on_b2, wait_on_b3]

    todos = list(
        zip(
            cycle(funcs),
            ((i, randint(1, 4)) for i in range(10))
        )
    )
    d = 2

    with ThreadPoolExecutor() as executor:
        for func, args in todos:
            executor.submit(func, *args)


