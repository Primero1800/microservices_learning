import asyncio

import httpx
from httpx import RequestError, HTTPStatusError

async def main():

    response = None
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get('https://primero1800.store')
            response.raise_for_status()
        except (RequestError, HTTPStatusError) as error:
            print(f' Вай-вай-вай. {error} упаль, однако')

    if response:
        print(response.status_code)
        [print(k, ': ',  v, sep='') for (k, v) in response.headers.items()]

if __name__ == "__main__":

    asyncio.run(main())