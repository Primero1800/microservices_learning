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

    def items(self):
        return self.params.items()

    def to_dict(self):
        return {key: value for key, value in self.items()}


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


def callback(task, kwargs=None):

    print('\n*****************************************************************************************************\n')
    print(kwargs['name']) if kwargs and 'name' in kwargs else print('Noname')

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
                name=url)
            for url in urls
        ]

        [contexted_task.task.add_done_callback(partial(callback, kwargs=contexted_task.to_dict())) for contexted_task in contexted_tasks]

        results = await asyncio.gather(*(contexted_task.task for contexted_task in contexted_tasks))


if __name__ == "__main__":

    asyncio.run(main())





