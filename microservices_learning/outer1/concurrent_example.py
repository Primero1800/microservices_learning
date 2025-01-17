import asyncio
import itertools

TEXT = 'abra12vg3nj4h56kl7lo8p9'

async def worker_letter(text):
    for symbol in text:
        if symbol.isalpha():
            print(symbol, end='')
        await asyncio.sleep(0.5)

async def worker_digit(text):
    for symbol in text:
        if symbol.isdigit():
            print(symbol, end='')
        await asyncio.sleep(0.5)


async def main():
    workers = (worker_letter, worker_digit)
    tasks = [asyncio.create_task(task(TEXT)) for task in workers]

    await asyncio.gather(*tasks)

if __name__ == "__main__":
    print(TEXT)

    asyncio.run(main())