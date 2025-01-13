from collections.abc import Iterable


def flatten(iterable):
    if isinstance(iterable, Iterable) and not isinstance(iterable, str):
        for item in iterable:
            if isinstance(item, Iterable) and not isinstance(item, str):
                yield from flatten(item)
            else:
                yield item
    else:
        yield iterable


if __name__ == "__main__":

    to_iter = [1, '23', 45, (6, ), [7, 8, '910', 11], (12, 13, ), 14]
    to_iter = 'ddddd'

    [print(n, end = ' ') for n in flatten(to_iter)]