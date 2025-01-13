import sys, warnings

if __name__ == "__main__":

    if sys.version_info[0] < 4:
        warnings.warn(
            "Для выполнения этой программы необходима как минимум версия Python 3.0",
            RuntimeWarning,
        )
    else:
        print('Нормальное продолжение')