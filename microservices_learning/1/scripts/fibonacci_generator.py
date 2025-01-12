class Fibonacci:
    def __init__(self, n=1):
        self._fibonacci_numbers = iter(self._fibonacci())
        self._seq = [next(self._fibonacci_numbers) for _ in range(n)]

    @staticmethod
    def fibonacci():
        a, b = 0, 1
        while True:
            yield b
            a, b = b, a + b

    def _fibonacci(self):
        return Fibonacci.fibonacci()

    def as_list(self):
        return self._seq

    def __iter__(self):
        yield from self._seq


if __name__ == "__main__":

    fibonacci_seq = Fibonacci(22)

    fibonacci_numbers = iter(Fibonacci.fibonacci())
    for i in range(25):
        print(next(fibonacci_numbers), end=' ')

    print()
    print(fibonacci_seq.as_list())

    print(*fibonacci_seq)






    # print()
    # fibonacci_seq = FibonacciSeq(25)
    # print(fibonacci_seq.)