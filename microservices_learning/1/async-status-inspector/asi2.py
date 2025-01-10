import asyncio
import urllib.parse

URLS = [
    'https://www.google.com/',
    'https://www.youtube.com/',
    'https://www.facebook.com/',
    'https://twitter.com/',
    'https://www.instagram.com/',
    'https://www.baidu.com/',
    'https://www.wikipedia.org/',
    'https://yandex.ru/',
    'https://yahoo.com/',
    'https://www.whatsapp.com/',

    'http://government.ru/structure/',
    'https://habr.com/ru/companies/wunderfund/articles/715126/',
    'https://www.youtube.com/watch?v=5_9x7czHJOM',
    'https://cp.beget.com/main/',
    'https://primero1800.store/',
    'https://football.kulichki.net/',
]


class OpenConnectionManager:
    def __init__(self, url_parsed):
        self.url_parsed = url_parsed

    async def __aenter__(self):
        if self.url_parsed.scheme == 'https':
            reader, writer = await asyncio.open_connection(
                host=self.url_parsed.hostname, port=443, ssl=True,
            )
        else:
            reader, writer = await asyncio.open_connection(
                host=self.url_parsed.hostname, port=80,
            )
        self.writer = writer
        self.reader = reader
        return (reader, writer, )

    async def __aexit__(self, exc_type, exc, tb):
        self.writer.close()

async def _send_request(writer, url_parsed):
    query = f'GET {url_parsed.path} HTTP/1.1\r\nHost: {url_parsed.hostname}\r\n\r\n'
    writer.write(query.encode('utf-8'))
    await writer.drain()


async def _get_response(reader):
    response = await reader.readline()
    return response.decode('utf-8').strip()


async def request_for_responce(reader, writer, url_parsed):
    await _send_request(writer, url_parsed)
    return await _get_response(reader)


async def get_status(url):
    url_parsed = urllib.parse.urlsplit(url)

    async with OpenConnectionManager(url_parsed) as (reader, writer):
        status = await request_for_responce(reader, writer, url_parsed)

    return status


async def main():
    tasks = [asyncio.create_task(get_status(url), name=url) for url in URLS]

    while tasks:
        done, tasks = await asyncio.wait(tasks, return_when=asyncio.FIRST_COMPLETED)
        for completed_task in done:
            print(f'{completed_task.get_name():30}:\t{completed_task.result()}')


if __name__ == "__main__":
    asyncio.run(main())