import os
import sys
from pathlib import Path, PurePath
from time import sleep

if __name__ == "__main__":

    current_directory = os.getcwd()

    print(current_directory)
    contents = os.listdir(current_directory)
    print("Содержимое текущей директории:")

    for item in contents:
        print(item)

    print('**************************************************************************************')
    p = Path('.')
    [print(x) for x in p.iterdir() if x.is_dir()]
    print('*****************', PurePath(p))




