import asyncio

class StartClient:
    def __init__(self, host, port):
        self.host = host
        self.port = port

    async def __aenter__(self):
        reader, writer = await asyncio.open_connection(
            host=self.host,
            port=self.port,

        )
        self.reader = reader
        self.writer = writer
        return (reader, writer, )

    async def __aexit__(self, exc_type, exc, tb):
        self.writer.close()
        await self.writer.wait_closed()


async def start_talking(reader, writer):
    escape = False
    while True:
        data = input()
        if data == 'q':
            data = 'client escaped\n'.encode('utf-8')
            escape = True
        else:
            data = (data + '\n').encode('utf-8')

        writer.write(data)
        await writer.drain()
        reply = await reader.read(128)
        print(reply.decode('utf-8'))

        if escape:
            break


async def main():
    async with StartClient(host='localhost', port=8000) as (reader, writer):
        await start_talking(reader, writer)


if __name__ == "__main__":
    asyncio.run(main())
