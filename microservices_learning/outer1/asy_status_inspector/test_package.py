import asyncio
import urllib
from functools import partial

import pytest_asyncio
import pytest
from unittest.mock import Mock

from outer1.asy_status_inspector.asi3 import _get_response, _send_request

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
        'Однажды в студеную зимнюю пору ',
        'я из лесу вышел - был сильный мороз... \n',
        'гляжу: поднимается медленно в гору лошадка, \r\n',
        'везущая хворосту воз\r ',
        '',
        'rr\r\n',
    ]
    index = -1
    async def read_data():
        nonlocal test_cases
        nonlocal index
        await asyncio.sleep(0)  # Не блокирующий режим чтения
        index += 1
        return test_cases[index].encode('utf-8')

    reader.readline.side_effect = read_data

    for i in range(len(test_cases)-1):
        result = await _get_response(reader)
        assert result == test_cases[i].strip().strip('\n').strip('\r')

    assert await _get_response(reader) == 'rr'


@pytest.mark.asyncio
async def test_send_request():
    writer = Mock(spec=asyncio.StreamWriter)

    buffer = []
    drained = []

    def _write(query):
        nonlocal buffer, drained
        drained.clear()
        buffer.append(query)
    #writer.write.side_effect = partial(_write, query)
    writer.write.side_effect = _write

    async def _drain():
        nonlocal buffer
        result = [part for part in buffer]
        await asyncio.sleep(0)
        buffer.clear()
        drained.append(result[0])
    writer.drain.side_effect = _drain

    url_parsed = urllib.parse.urlsplit('http://primero1800.store')
    await _send_request(writer, url_parsed)
    assert len(drained) > 0
    assert len(buffer) == 0
    assert drained.pop() == b'GET  HTTP/1.1\r\nHost: primero1800.store\r\n\r\n'

    url_parsed = urllib.parse.urlsplit('http://football.kulichki.net')
    await _send_request(writer, url_parsed)
    assert len(drained) > 0
    assert len(buffer) == 0
    assert drained.pop() == b'GET  HTTP/1.1\r\nHost: football.kulichki.net\r\n\r\n'

