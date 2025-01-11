from ctypes import c_bool
import time
from datetime import datetime
from random import randint
from multiprocessing import Process, Lock, Value, Queue

WORKERS = 6

COUNTER = Value('i', 0)
FINISH = Value(c_bool, False)

lock = Lock()

class LQueue:
    def __init__(self, buffer):
        self.buffer = buffer

    def getall(self):
        result = []
        while not self.buffer.empty():
            result.append(self.buffer.get())
        return result

    def __iter__(self):
        yield from self.getall()


pr_queue = LQueue(Queue())


def counter_worker(name, counter, finish, buffer):
    inner_counter = 0
    with lock:
        print(f'{name} started')
    start_time = datetime.now()

    while True:
        time.sleep(randint(1,4))
        inner_counter += 1
        with lock:
            counter.value += 1
            if finish.value:
                print(f'{name} finished')
                break

    print(f"{name} ** {inner_counter} ** {datetime.now() - start_time}")
    data = (name, inner_counter, datetime.now() - start_time)
    buffer.put(data)
    d = 2


if __name__ == "__main__":

    print('Создание потоков:')

    procs = [
        Process(
            target=counter_worker,
            name=f"proc_{i}",
            args=(f"proc_{i}", COUNTER, FINISH, pr_queue.buffer),
        ) for i in range(WORKERS)
    ]
    time.sleep(0.5)

    [print(f'Создан: {proc.name}') for proc in procs]
    time.sleep(0.3)

    print()
    print('Запуск процессов')
    [proc.start() for proc in procs]

    time.sleep(0.5)
    print()
    time.sleep(randint(10, 15))
    with lock:
        FINISH.value = True

    d = 2
    [proc.join() for proc in procs]

    print()
    print('GLOBAL COUNTER:', COUNTER.value)
    d = 2
    results = sorted(pr_queue)
    [print(f"{el[0]}: counter={el[1]}, worked={el[2]}") for el in results]



