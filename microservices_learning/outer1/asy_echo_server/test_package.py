import asyncio
import pytest
from unittest.mock import MagicMock, Mock

from outer1.asy_echo_server import async3


# Установите область видимости цикла событий для всех асинхронных фикстур
pytest_plugins = ['pytest_asyncio']
pytest_asyncio_enable_loop = True

@pytest.fixture(scope='function')
def asyncio_default_fixture_loop_scope(request):
    return 'function'


@pytest.mark.asyncio
async def test_start_talking():
    # Имитация reader и writer
    reader = Mock(spec=asyncio.StreamReader)
    writer = Mock(spec=asyncio.StreamWriter)

    # Настройка side_effect для reader.read, чтобы имитировать получение данных
    async def read_data(size):
        await asyncio.sleep(0)  # Не блокирующий режим чтения
        return 'Тестовый ответ от сервера\n'.encode('utf-8')
    reader.read.side_effect = read_data

    # Тестирование до момента выхода (когда вводится 'q')
    # Взаимодействие с input() и writer.write через магическую имитацию
    input_call_count = 0
    def mock_input(prompt=None):
        nonlocal input_call_count
        input_values = ['Привет', 'q']  # Значения, которые будут возвращены input()
        result = input_values[input_call_count]
        input_call_count += 1
        return result

    # Запуск тестируемой функции
    await async3.start_talking(mock_input, writer)

    # Проверка вызовов writer.write
    assert writer.write.call_count == 2  # 'Привет' и 'client escaped'

    # Проверка содержимого writer
    writer.write.assert_any_call('Привет\n'.encode('utf-8'))
    writer.write.assert_any_call(b'client escaped\n')

    # Проверка выхода из цикла при вводе 'q'
    assert input_call_count == 1  # Должен быть вызван ровно один раз

    # Проверка переданных значений в writer.write и input()
    writer.write.assert_called_with('Привет\n'.encode('utf-8'))
    writer.write.assert_called_once_with(b'client escaped\n')
    mock_input.assert_called_once_with('server: ')


