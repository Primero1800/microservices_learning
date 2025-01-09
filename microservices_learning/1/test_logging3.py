import logging
import sys

# Настройка логирования
logging.basicConfig(
    filename=f'{__file__}.err',  # Имя файла для записи логов
    level=logging.ERROR,     # Уровень логирования
    format='%(asctime)s - %(levelname)s - %(message)s'  # Формат лога
)

# Перехват ошибок
class ErrorCatcher:
    def __init__(self):
        self.buffer = ''

    def write(self, message):
        d = 2
        if message and message not in ('', ' ', '\n'):
            self.buffer += message.strip() + '\n'

    def flush(self):
        if self.buffer:
            logging.error(self.buffer)
            self.buffer =''


sys.stderr = ErrorCatcher()



if __name__ == "__main__":

    logging.debug('swinya')
    #input()
    logging.error('Baran')
    #input()

    10 / 0