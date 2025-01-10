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


# class OpenConnectionManager:
#     def __init__(self, url):
#         self.parsed_url = urllib.parse.urlsplit(url)
#         self.host = self.parsed_url.hostname
#         if self.parsed_url.scheme == 'http':
#             self.port = 80
#         else:
#             self.port = 443
#
#     async def __aenter__(self):
#         if self.port == 443:
#             reader, writer = await asyncio.open_connection(
#                 host=self.host,
#                 port=self.port,
#                 ssl=True,
#             )
#         else:
#             reader, writer = await asyncio.open_connection(
#                 host=self.host,
#                 port=self.port,
#             )
#
#         self.reader = reader
#         self.writer = writer
#         return (reader, writer, {
#             'host': self.host,
#             'path': self.parsed_url.path,
#         })
#
#     async def __aexit__(self, exc_type, exc, tb):
#         self.writer.close()
#         await self.writer.wait_closed()


async def request_for_responce(reader, writer, params):

    query = f"GET {params['path']} HTTP/1.1\r\nHost: {params['host']}\r\n\r\n"
    writer.write(query.encode())
    await writer.drain()

    response = await reader.readline()
    status = response.decode().strip()
    return status


async def get_status(url):

    url_parsed = urllib.parse.urlsplit(url)

    if url_parsed.scheme == 'https':
        reader, writer = await asyncio.open_connection(
            host=url_parsed.hostname, port=443, ssl=True,
        )
    else:
        reader, writer = await asyncio.open_connection(
            host=url_parsed.hostname, port=80,
        )

    query = f'GET {url_parsed.path} HTTP/1.1\r\nHost: {url_parsed.hostname}\r\n\r\n'
    writer.write(query.encode())
    await writer.drain()
    response = await reader.readline()
    writer.close()
    status = response.decode().strip()

    return status


async def main():

    for url in URLS:
        status = await get_status(url)
        print(f'{url:30}:\t{status}')


if __name__ == "__main__":
    asyncio.run(main())