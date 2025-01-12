
MAXIMUM = 100

DICTIONARY = {
    'fizz': 'fizz',
    'buzz': 'buzz',
    'fizzbazz': 'fizzbazz',
}


def reject_message(message, *args):
    print(message, end='\n\n')
    return [None for _ in args]

def accepted_message(message):
    print(message, end='\n\n')


def get_limit(maximum):
    limit = None

    while not limit:
        limit = input(f"Enter positive integer limit (0 < limit <= {maximum}) for FizzzBuzz test: ")
        try:
            limit = int(limit)
        except ValueError:
            (limit, ) = reject_message(f'TypeError, enter {type(1)}, not {type(limit)}.', limit)
        if limit and limit > maximum:
            (limit, ) = reject_message(f'ValueError, limit must be in range from 0 to {maximum}, not {limit}.', limit)
    accepted_message(f"limit accepted: {limit}")
    return limit

def get_fizzbuzz(limit):
    fizz, buzz = None, None

    while not fizz or not buzz:
        print(f"(NOTE) require conditions: 0 < fizz < buzz < fizz*buzz < {limit}. ")
        fizzbuzz = input(f"Enter positive integers fizz and buzz for FizzzBuzz test (scheme: fizz, buzz): ")

        try:
            fizz, buzz = fizzbuzz.split(', ')
        except ValueError:
            fizz, buzz = reject_message(f'Expression does match sceme: fizz, buzz. fizz={fizz}, buzz={buzz}', fizz, buzz)
        else:
            try:
                fizz, buzz = int(fizz), int(buzz)
            except ValueError:
                fizz, buzz = reject_message(f'TypeError, enter {type(1)}, not fizz is {type(fizz)} and buzz is {type(buzz)}.', fizz, buzz)
            else:
                if not 0 < fizz < buzz < fizz * buzz < limit:
                    fizz, buzz = reject_message(f"Values don't match expression 0 < {fizz} < {buzz} < {fizz * buzz} < {limit}", fizz, buzz)

    accepted_message(f"fizz and buzz accepted: {fizz}, {buzz}")
    return fizz, buzz


def get_NOD(b, a):
    while b != 0:
        a, b = b, a % b
    return a

def get_NOK(b, a):
    module = abs(a*b)
    return module // get_NOD(b, a)


def get_fizzbuzz_value(fizz, buzz):
    return get_NOK(fizz, buzz)


def start_fizzbuzz(limit, fizz, buzz):
    fizzbuzz = get_fizzbuzz_value(fizz, buzz)
    for i in range(1, limit+1):
        if not i % fizzbuzz:
            print(i, DICTIONARY['fizzbazz'])
        elif not i % buzz:
            print(i, DICTIONARY['buzz'])
        elif not i % fizz:
            print(i, DICTIONARY['fizz'])
        else:
            print(i)



if __name__ == "__main__":

    limit = get_limit(MAXIMUM)
    fizz, buzz = get_fizzbuzz(limit)
    start_fizzbuzz(limit, fizz, buzz)
