from itertools import count


class NumberOdd:
    def __init__(self, limit):
        self._limit = limit

    def __iter__(self):
        yield from range(2, self._limit+1, 2)


if __name__ == "__main__":

    no = NumberOdd(47)

    sentinel = object()
    it = iter(range(2, 47+1, 2))

    while True:
        element = next(it, sentinel)
        if element is not sentinel:
            print(element, end=' ')
        else:
            print()
            break

    it2 = iter(count(0, 2))

    while True:
        element = next(it2)
        if input() != 'q':
            print(element, end=' ')
        else:
            break
