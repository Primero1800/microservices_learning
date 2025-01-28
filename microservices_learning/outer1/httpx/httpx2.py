import asyncio

import httpx
from httpx import RequestError, HTTPStatusError

API_KEY = '66718dcc-6a33-43bf-9e85-73d7f9a3e7f2'
ENDPOINT = 'https://api.deepai.org/api/text-generator'


async def main():

    while True:
        responce = None
        question = input("Ваш вопрос: ")
        if not question:
            break
        data = {
            "text": question,
            "api_key": API_KEY,
        }
        try:
            response = httpx.post(
                    ENDPOINT,
                    json=data,
                    headers={"Api-Key": API_KEY},
                    timeout=20,
            )
            print('TRY', response.status_code)
            d = 2
            response.raise_for_status()
        except (RequestError, HTTPStatusError) as error:
            print(f' Вай-вай-вай. {error} упаль, однако')
            print('EXC', response.status_code)

        if response:
            print(response.text)


if __name__ == "__main__":

    asyncio.run(main())