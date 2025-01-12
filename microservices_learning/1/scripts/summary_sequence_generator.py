

def brute_sequence(n):
    if n < 0:
        return 0
    res = [0, 1]
    if n in (0, 1):
        return res[n]
    while len(res)  < n + 1:
        res.append(sum(res))
    return res[n], res


def smart_sequence(n):
    if n < 0:
        return 0
    if n in (0, 1):
        return n
    return 2**(n-2)


def recursion_sequence(n):
    if n == 0:
        return 0
    if n == 1:
        return 1
    return sum(recursion_sequence(i) for i in range(n))

if __name__ == "__main__":


    print(brute_sequence(n))
    print(smart_sequence(n))