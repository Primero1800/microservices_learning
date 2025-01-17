import logging
import sys

original_stderr = sys.stderr
file_err = open(f"{__file__}.err", 'a')
sys.stderr = file_err




if __name__ == "__main__":

    logger = logging.getLogger()
    logger.setLevel(logging.INFO)


    formatter = logging.Formatter('%(asctime)s | %(levelname)s | %(message)s')

    stdout_handler = logging.StreamHandler(sys.stderr)
    stdout_handler.setLevel(logging.DEBUG)
    stdout_handler.setFormatter(formatter)

    file_handler = logging.FileHandler(f"{__file__}.log")
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(stdout_handler)

    logger.warning("Preved, medved")


    test_dict = {}
    print(test_dict['test'], 10/0)


    sys.stderr = original_stderr
    file_err.close()