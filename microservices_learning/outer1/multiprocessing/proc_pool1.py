from concurrent.futures import ProcessPoolExecutor


def adder(x, y):
    print('adder')
    return x + y


def multer(x, y):
    print('multer')
    return x * y


def differ(x, y):
    print('differ')
    return x - y


def divider(x, y):
    print('divider')
    return x // y


def greeter(x , y):
    print('greeter')
    return f"greet {x} and {y}"


def slipper(x, y):
    print('slipper')
    return f"{x}{y}"


def starter(args):
    func, *args = args
    return func(*args)


funcs = [adder, multer, differ, divider, greeter, slipper]
params = (6, 2)


if __name__ == "__main__":

    args = [(func, *params) for func in funcs]
    d = 2

    with ProcessPoolExecutor() as pool:
        results = pool.map(starter, args)

    for result in results:
        print(result)