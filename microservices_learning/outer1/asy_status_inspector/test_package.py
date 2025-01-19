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


@pytest.mark.parametrize(
    ('entered', 'expected'),
    [
        ('Однажды в студеную зимнюю пору ', 'Однажды в студеную зимнюю пору'),
        ('я из лесу вышел - был сильный мороз... \n', 'я из лесу вышел - был сильный мороз...'),
        ('гляжу: поднимается медленно в гору лошадка, \r\n', 'гляжу: поднимается медленно в гору лошадка,'),
        ('везущая хворосту воз\r ', 'везущая хворосту воз'),
        ('', ''),
        ('rr\r\n', 'rr'),
    ]
)
@pytest.mark.asyncio
async def test_get_response(entered, expected):
    reader = Mock(spec=asyncio.StreamReader)

    async def read_data():
        await asyncio.sleep(0)
        return entered.encode('utf-8')
    reader.readline.side_effect = read_data

    assert await _get_response(reader) == expected


@pytest.mark.parametrize(
    ('entered', 'expected'),
    [
        ('http://primero1800.store', b'GET  HTTP/1.1\r\nHost: primero1800.store\r\n\r\n'),
        ('http://football.kulichki.net', b'GET  HTTP/1.1\r\nHost: football.kulichki.net\r\n\r\n'),
    ]
)
@pytest.mark.asyncio
async def test_send_request(entered, expected):
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

    url_parsed = urllib.parse.urlsplit(entered)
    await _send_request(writer, url_parsed)
    assert len(drained) > 0
    assert len(buffer) == 0
    assert drained.pop() == expected


@pytest.mark.asyncio
@pytest.mark.cls
@pytest.mark.parametrize(
    ('URL', 'hostname', 'scheme', 'status'),
    [
        ('https://www.google.com/', 'www.google.com', 'https', 'HTTP/1.1 200 OK'),
        ('http://government.ru/structure/', 'government.ru', 'http', 'HTTP/1.1 200 OK'),
        ('https://www.youtube.com/watch?v=5_9x7czHJOM', 'www.youtube.com', 'https', 'HTTP/1.1 301 Moved Permanently'),
        ('https://primero1800.store/', 'primero1800.store', 'https', 'HTTP/1.1 200 OK'),
        ('default', None, '', 'HTTP/1.1 400 Bad Request'),
        ('http://invalid', 'invalid', 'http', '[Errno -2] Name or service not known'),
    ]
)
async def test_get_status(URL, hostname, scheme, status):

    status_to_assert = await get_status(URL)
    cm = OpenConnectionManager(urllib.parse.urlsplit(URL))

    assert cm.url_parsed.hostname == hostname
    assert cm.url_parsed.scheme == scheme
    assert status_to_assert == status








