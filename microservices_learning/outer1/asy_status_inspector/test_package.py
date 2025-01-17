import asyncio
import urllib
import pytest
from unittest.mock import Mock

from outer1.asy_status_inspector.asi3 import _get_response, _send_request, OpenConnectionManager, get_status

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


@pytest.mark.asyncio
@pytest.mark.cls
async def test_get_status():
    URLS = [
        'https://www.google.com/',
        'http://government.ru/structure/',
        'https://www.youtube.com/watch?v=5_9x7czHJOM',
        'https://primero1800.store/',
        'default',
        'http://invalid'
    ]

    statuses = [await get_status(url) for url in URLS]
    cms = [OpenConnectionManager(urllib.parse.urlsplit(url)) for url in URLS]

    assert cms[1].url_parsed.hostname == 'government.ru'
    assert cms[2].url_parsed.hostname == 'www.youtube.com'
    assert cms[3].url_parsed.hostname == 'primero1800.store'
    assert cms[4].url_parsed.hostname is None
    assert cms[5].url_parsed.hostname == 'invalid'

    assert cms[0].url_parsed.scheme == 'https'
    assert cms[1].url_parsed.scheme == 'http'
    assert cms[4].url_parsed.scheme == ''
    assert cms[5].url_parsed.scheme == 'http'

    assert statuses[0]  == 'HTTP/1.1 200 OK'
    assert statuses[1] == 'HTTP/1.1 200 OK'
    assert statuses[2] == 'HTTP/1.1 301 Moved Permanently'
    assert statuses[3] == 'HTTP/1.1 200 OK'
    assert statuses[4] == 'HTTP/1.1 400 Bad Request'
    assert statuses[5] == '[Errno -2] Name or service not known'








