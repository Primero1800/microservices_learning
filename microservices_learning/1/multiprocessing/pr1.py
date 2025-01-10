import json
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
from datetime import datetime


jsonSize = 5000000
count = 8


def timed(func):
    def wrapper(*args, **kwargs):
        start_time = datetime.now()
        result = func(*args, **kwargs)
        print(f"{func.__name__} worked: {datetime.now()-start_time}")
        return result
    return wrapper



def hard_work(size):
        json.dumps(list(range(size)))
        return 1


@timed
def sequential(size, count):
    result = []
    for _ in range(count):
        result.append(hard_work(size))
    return result


@timed
def run_threads(size, executionUnitsCount):
    with ThreadPoolExecutor() as executor:
        results = list(executor.map(hard_work, [size] * executionUnitsCount))
    return results



@timed
def run_processes(size, executionUnitsCount):
    with ProcessPoolExecutor() as executor:
        results = list(executor.map(hard_work, [size] * executionUnitsCount))
    return results


if __name__ == "__main__":
    for i in range(count):
        print(f"FOR {jsonSize} and {i} tasks:")
        print(sequential(jsonSize, i))
        print(run_threads(jsonSize, i))
        print(run_processes(jsonSize, i))
        print()




