import asyncio
import random
import time


async def tasked(name):
    print(f'{name}-tasked started')
    random_sleep = random.randint(1, 2)
    await asyncio.sleep(random_sleep)
    return f'{name}-tasked ************************************{random_sleep}'

async def usual(name=0):
    print(f'{name}-usual started')
    await asyncio.sleep(1)
    return f'{name} - usual uuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuu 5'

async def main():

    tasks = [asyncio.create_task(tasked(i)) for i in range(1, 8)]
    tasks.append(asyncio.create_task(usual()))


    running = tasks
    while running:
        completed, running = await asyncio.wait(running, return_when=asyncio.FIRST_COMPLETED)

        for task in completed:
            print(task.result())

    process = await asyncio.create_subprocess_exec('ls', stdout=asyncio.subprocess.PIPE, stdin=asyncio.subprocess.PIPE)
    process.stdin.write(b'zhopa')

    bline = await process.stdout.read()
    d = 2
    lines = str(bline, encoding='utf-8').split('\n')
    print()
    print(*lines, sep='\n')
    await process.wait()

    not_exit = True
    while not_exit:
    #process2 =  await asyncio.create_subprocess_shell('cat outer1.py | wc -l', stdin=asyncio.subprocess.PIPE, stdout=asyncio.subprocess.PIPE)
        command = input()
        if command == 'q':
            break
        process2 = await asyncio.create_subprocess_shell(command)
        d = 2
        await process2.wait()



if __name__ == "__main__":
    asyncio.run(main())
    #asyncio.get_event_loop().run_until_complete(main())
