import asyncio
import pytest_asyncio
import pytest
from unittest.mock import Mock

from outer1.asy_status_inspector.asi3 import _get_response


# Установите область видимости цикла событий для всех асинхронных фикстур
pytest_plugins = ['pytest_asyncio']
pytest_asyncio_enable_loop = True

@pytest.fixture(scope='function')
def asyncio_default_fixture_loop_scope(request):
    return 'function'

@pytest.mark.asyncio
async def test_get_response():
    reader = Mock(spec=asyncio.StreamReader)

    test_cases = [
        'Однажды в студеную зимнюю пору',
        'я из лесу вышел - был сильный мороз...',
        'гляжу: поднимается медленно в гору лошадка,',
        'везущая хворосту воз',
        '',
        'rr\n',
    ]
    index = -1
    async def read_data():
        nonlocal test_cases
        nonlocal index
        await asyncio.sleep(0)  # Не блокирующий режим чтения
        index += 1
        return test_cases[index].encode('utf-8')

    reader.read.side_effect = read_data
    reader.readline.side_effect = read_data

    for i in range(len(test_cases)-1):
        result = await _get_response(reader)
        assert result == test_cases[i]

    assert await _get_response(reader) == 'rr'
