import logging
import sys

# Настройка логирования
# logging.basicConfig(
#     filename=f"{__file__}.err",  # Имя файла для записи логов
#     level=logging.ERROR,     # Уровень логирования
#     format='%(asctime)s - %(levelname)s - %(message)s'  # Формат лога
# )


original_stderr = sys.stderr
file_err = open(f"{__file__}.err", 'a')
sys.stderr = file_err

logger = logging.getLogger()
logger.setLevel(logging.INFO)

stdout_handler = logging.StreamHandler(sys.stderr)
stdout_handler.setLevel(logging.DEBUG)
stdout_handler.setFormatter('%(asctime)s - %(levelname)s - %(message)s')
logger.addHandler(stdout_handler)


if __name__ == "__main__":

    10 / 0

    sys.stderr = original_stderr
    file_err.close()
