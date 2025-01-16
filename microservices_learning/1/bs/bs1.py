import asyncio
import urllib.parse

import httpx
from bs4 import BeautifulSoup
from httpx import RequestError, HTTPStatusError

URL = 'https://www.primero1800.store'

class SiteParser:
    def __init__(self, url):
        self.url = url
        self.get_host()
        self.html = None

    def get_host(self):
        parsed =  urllib.parse.urlsplit(self.url)
        self.hostname = parsed.hostname
        self.scheme = parsed.scheme
        self.path = f"{self.scheme}://{self.hostname}"

    def create_url(self, url):
        return f"{self.path}{url}"

    async def load_html(self):
        self.html = await self._get_html()

    async def _get_html(self):
        async with httpx.AsyncClient() as client:
            try:
                result = await client.get(self.url)
                result.raise_for_status()
                return result.text
            except (RequestError, HTTPStatusError) as error:
                print(f' Вай-вай-вай. {error} упаль, однако')
                return False

    def parse_site(self):
        soup = BeautifulSoup(self.html, 'html.parser')
        print(soup.prettify())
        img_list = soup.findAll('img')
        imgs = []
        try:
            for img in img_list:
                if 'data-echo' in img.attrs:
                    imgs.append(self.create_url(img.attrs['data-echo']))
                elif 'src' in img.attrs:
                    imgs.append(self.create_url(img.attrs['src']))
        except (KeyError, AttributeError, TypeError) as error:
            print(f'Raised error: {error} while parsing. Result may be not valid')
        return imgs




async def main():
    sp = SiteParser(URL)
    await sp.load_html()
    imgs = sp.parse_site()
    print(*imgs, sep='\n')


if __name__ == "__main__":

    asyncio.run(main())
