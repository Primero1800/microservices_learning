import queue
import time
from datetime import datetime
from random import randint
from threading import Lock, Thread

WORKERS = 6
COUNTER = 0
FINISH = False

lock = Lock()
th_queue = queue.Queue()

def counter_worker(name):
    inner_counter = 0
    global COUNTER, FINISH
    with lock:
        print(f'{name} started')
    start_time = datetime.now()

    while True:
        time.sleep(randint(1,4))
        inner_counter += 1
        with lock:
            #if inner_counter > COUNTER:
            COUNTER += 1
            if FINISH:
                print(f'{name} finished')
                break
    th_queue.put((name, inner_counter, datetime.now() - start_time))


if __name__ == "__main__":

    print('Создание потоков:')

    threads = [
        Thread(
            target=counter_worker,
            name=f"thread_{i}",
            args=(f"thread_{i}", ),
        ) for i in range(WORKERS)
    ]
    time.sleep(0.5)

    [print(f'Создан: {th.name}') for th in threads]
    time.sleep(0.3)

    print()
    print('Запуск потоков')
    [th.start() for th in threads]

    print()
    time.sleep(randint(10, 15))
    with lock:
        FINISH = True

    [th.join() for th in threads]
    print()
    print('GLOBAL COUNTER:', COUNTER)
    results = sorted(th_queue.queue)
    [print(f"{el[0]}: counter={el[1]}, worked={el[2]}") for el in results]



