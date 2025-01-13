import platform
import sys

if __name__ == "__main__":

    print("Загруженные модули:")
    for module in sys.modules:
        print(module)