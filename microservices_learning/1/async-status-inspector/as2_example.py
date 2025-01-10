import asyncio
from urllib.parse import urlsplit


async def get_status(url):

    url_parsed = urlsplit(url)
    if url_parsed.scheme == 'https':
        reader, writer = await asyncio.open_connection(url_parsed.hostname, 443, ssl=True)
    else:
        reader, writer = await asyncio.open_connection(url_parsed.hostname, 80)
    query = f'GET {url_parsed.path} HTTP/1.1\r\nHost: {url_parsed.hostname}\r\n\r\n'
    writer.write(query.encode())
    await writer.drain()
    response = await reader.readline()
    writer.close()
    status = response.decode().strip()
    return status


# главная корутина
async def main():
    # список из 10 самых посещаемых сайтов, которые нужно проверить
    sites = [
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

    # проверка кодов HTTP-состояния для всех сайтов
    for url in sites:
        # получение кода состояния для URL
        status = await get_status(url)
        # вывод URL и его кода состояния
        print(f'{url:30}:\t{status}')


# запуск asyncio-программы
asyncio.run(main())