import asyncio
from asyncio import StreamReader, StreamWriter


async def main():
    reader: StreamReader
    writer: StreamWriter
    reader, writer= await asyncio.open_connection(
        host='localhost',
        port=8000,
    )

    escape = False
    while True:
        data = input()
        if data == 'q':
            data = 'client escaped'.encode('utf-8')
            escape = True
        else:
            data = data.encode('utf-8')

        writer.write(data)
        await writer.drain()
        reply = await reader.read(128)
        print(reply.decode('utf-8'))

        if escape:
            break


if __name__ == "__main__":
    asyncio.run(main())
