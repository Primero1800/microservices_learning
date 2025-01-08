from itertools import count

module_singleton_object = None
module_singleton_instances = {}

class Singleton(object):
    _instance = None
    def __new__(cls, *args, **kwargs):
        global module_singleton_object
        if not isinstance(cls._instance, cls):
        #if not module_singleton_object and not isinstance(cls._instance, cls):
            cls._instance = super().__new__(cls, *args, **kwargs)
            #module_singleton_object = cls._instance
        return cls._instance
        #return module_singleton_object


def singleton(class_):
    #_instances = {}
    global module_singleton_instances
    def getinstance(*args, **kwargs):
        #if class_ not in _instances:
        if not module_singleton_instances:
            #_instances[class_] = class_(*args, **kwargs)
            module_singleton_instances[class_] = class_(*args, **kwargs)
        #return list(_instances.values())[0] if _instances else None
        return list(module_singleton_instances.values())[0] if module_singleton_instances else None
    return getinstance

#@singleton
class Logger(Singleton):
    pass

#@singleton
class Supper(Singleton):
    pass


if __name__ == "__main__":

    l1 = Logger()
    l2 = Logger()
    s1 = Supper()
    s2 = Supper()

    print(l1, l2, s1, s2, l1 == l2)


    class NumberIterator:
        def __init__(self, limit):

            self._limit = limit

        def __iter__(self):
            return InnerIterator(self)

    class InnerIterator:
        def __init__(self, owner):
            self.n = 0
            self.owner = owner

        def __iter__(self):
            return self

        def __next__(self):
            self.n += 2
            if self.n > self.owner._limit:
                raise StopIteration
            return self.n


    ni = NumberIterator(82)

    for i in ni:
        print(i, sep='  ', end =' ')

    print()
    it = iter(NumberIterator(82))
    sentinel = object()
    while True:
        element = next(it, sentinel)
        if element is not sentinel:
            print(element)
        else:
            break





