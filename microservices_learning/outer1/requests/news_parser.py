import asyncio
import urllib.parse

import requests
from bs4 import BeautifulSoup, Tag


class News_Parser:
    def __init__(self):
        self.url = 'https://habr.com/ru/hub/python/'
        self.host = self.get_host()
        self.html = self.get_html()

    def get_host(self):
        parsed =  urllib.parse.urlsplit(self.url)
        return f"{parsed.scheme}://{parsed.hostname}"

    def get_html(self):
        try:
            result = requests.get(self.url)
            result.raise_for_status()
            return result.text
        except (requests.RequestException, ValueError) as ex:
            print('Server error', ex)
            return False

    def _get_python_raw_news(self):
        soup = BeautifulSoup(self.html, 'html.parser')
        news_list = soup.findAll('h2', class_='tm-title tm-title_h2')
        return news_list

    async def get_python_news(self):
        raw_list = self._get_python_raw_news()
        tasks = [asyncio.create_task(self.get_answer(raw_news)) for raw_news in raw_list]
        result = []

        while tasks:
            done, tasks = await asyncio.wait(tasks, return_when=asyncio.FIRST_COMPLETED)
            for done_task in done:
                result_string = done_task.result()
                print(result_string)
                result.append(result_string)
        return result

    async def get_answer(self, raw_news):
        task_link = await asyncio.create_task(self.get_python_news_link(raw_news))
        task_text = await asyncio.create_task(self.get_python_news_text(raw_news))
        return f"{task_link:40}  {task_text}"


    async def get_python_news_text(self, raw_str: Tag):
        await asyncio.sleep(0)
        try:
            return raw_str.text
        except (TypeError, AttributeError):
            return ''

    async def get_python_news_link(self, raw_str: Tag):
        await asyncio.sleep(0)
        try:
            href = raw_str.contents.pop(1).attrs['href']
            return f"{self.host}{href}"
        except (TypeError, AttributeError):
            return self.url


async def main():
    np = News_Parser()
    results = await np.get_python_news()

    #print(*results, sep='\n')



if __name__ == "__main__":
    asyncio.run(main())