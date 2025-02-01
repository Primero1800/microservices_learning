from outer1.ready_decorators.timed import timed

CYCLE = 1000
l = [0, 4, 7, 1, 5, 8, 9, 3, 4, 2, 4, 6, 3, 6] * CYCLE


@timed
def sort_brute(l):
    n = len(l)
    for i in range(n):
        for j in range(i+1, n):
            if l[j] < l[i]:
                l[i], l[j] = l[j], l[i]
    return l


@timed
def sort_buble(l):
    n = len(l)
    for i in range(n):
        changed = False
        for k in range(n - i - 1):
            if l[k] < l[k+1]:
                l[k], l[k+1] = l[k+1], l[k]
                changed = True
        if not changed:
            break
    return l


def sort_quick(l):
    if len(l) < 2:
        return l
    return sort_quick([n for n in l[1:] if n >= l[0]]) + [l[0]] + sort_quick([n for n in l[1:] if n < l[0]])


def sort_quick_optimized(l):
    if len(l) < 2:
        return l
    pivot = l[len(l) // 2]  # Опорный элемент - средний элемент
    left = [x for x in l if x < pivot]  # Элементы меньше опорного
    middle = [x for x in l if x == pivot]  # Элементы равные опорному
    right = [x for x in l if x > pivot]  # Элементы больше опорного
    return sort_quick_optimized(left) + middle + sort_quick_optimized(right)


@timed
def start_quicksort(l):
    sort_quick_optimized(l)


if __name__ == "__main__":
    l1 = l.copy()
    l2 = l.copy()
    l3 = l.copy()

    sort_brute(l1)
    sort_buble(l2)
    start_quicksort(l3)
