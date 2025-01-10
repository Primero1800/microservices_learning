import asyncio

async def handler(reader, writer):
    serve = True
    while serve:

        #data = await reader.read(128)
        data = await reader.readline()
        if data:
            message = data.decode()
            addr = writer.get_extra_info('peername')
            print(f"{addr[0]}:{addr[1]}# {message.strip('\n')}")

            message_back = (f"HTTP/1.0 200 OK ** {message.strip('\n')} received").encode('utf-8')
            writer.write(message_back)
            await writer.drain()
        else:
            serve = False
            writer.close()
            await writer.wait_closed()

    print("Close the client socket")



async def main():
    server = await asyncio.start_server(
        host='localhost',
        port=8000,
        client_connected_cb=handler,
    )

    addr = server.sockets[0].getsockname()
    print(f'Serving on {addr}')

    async with server:
        await server.serve_forever()


if __name__ == "__main__":
    asyncio.run(main())
