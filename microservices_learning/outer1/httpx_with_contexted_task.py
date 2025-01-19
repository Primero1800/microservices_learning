import asyncio
from functools import partial

import httpx
from httpx import UnsupportedProtocol

class ContextedTask:
    def __init__(self, task, **kwargs):
        self.task = task
        self.params = kwargs


    def __getitem__(self, item):
        return self.params[item]


class AsyncDataGetterClient(httpx.AsyncClient):
    async def get_data_from_url(self, url, headers=None):
        if not headers:
            headers = {"Accept": "application/json"}

        try:
            response = await self.get(url, headers=headers)
        except UnsupportedProtocol as error:
            return 400, None, error

        if response.status_code == 200:
            try:
                return response.status_code, response.json(), None
            except ValueError as error:
                return response.status_code, response.text, error
        else:
            return response.status_code, response.text, None


def callback(task, name=None):
    print('\n*****************************************************************************************************\n')
    print(name)
    print(task.result()[0])
    print(task.result()[1])
    print('jsonError: ', task.result()[2])


async def main():

    urls = [
        'https://www.example.com',
        'https://www.primero1800.store/api/v1/posts/',
        'invalid',
    ]


    async with AsyncDataGetterClient() as client:

        contexted_tasks = [
            ContextedTask(
                asyncio.create_task(
                    client.get_data_from_url(url), ),
                nnname=url)
            for url in urls
        ]
        [contexted_task.task.add_done_callback(partial(callback, name=contexted_task['nnname'])) for contexted_task in contexted_tasks]

        results = await asyncio.gather(*(contexted_task.task for contexted_task in contexted_tasks))



if __name__ == "__main__":

    asyncio.run(main())





