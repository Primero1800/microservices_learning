import aiohttp
import asyncio

async def fetch_data(session, url):
    async with session.get(url) as response:
        return await response.text()

async def main():
    urls = [
        "https://primero1800.store/api",

    ]
    async with aiohttp.ClientSession() as session:
        tasks = [fetch_data(session, url) for url in urls]
        results = await asyncio.gather(*tasks)
    for result in results:
        print(result)

asyncio.run(main())