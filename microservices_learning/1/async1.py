import asyncio
import random
import time


async def tasked(name):
    print(f'{name}-tasked started')
    random_sleep = random.randint(1, 8)
    await asyncio.sleep(random_sleep)
    return f'{name}-tasked ************************************{random_sleep}'

async def usual(name=0):
    print(f'{name}-usual started')
    await asyncio.sleep(5)
    return f'{name} - usual uuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuu 5'

async def main():

    tasks = [asyncio.create_task(tasked(i)) for i in range(1, 8)]
    tasks.append(asyncio.create_task(usual()))


    running = tasks
    while running:
        completed, running = await asyncio.wait(running, return_when=asyncio.FIRST_COMPLETED)
        for task in completed:
            print(task.result())



if __name__ == "__main__":
    asyncio.run(main())
