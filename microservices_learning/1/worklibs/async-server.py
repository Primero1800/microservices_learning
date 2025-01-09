import asyncio

async def handler(reader, writer):
    while (True):
        data = await reader.read(128)
        if data:
            message = data.decode()
            addr = writer.get_extra_info('peername')
            print("Received %r from %r" % (message, addr))
            #print(type(data))

            message_back = (f"HTTP/1.0 200 OK ** {message} received").encode('utf-8')
            writer.write(message_back)
            await writer.drain()
        else:
            print("Close the client socket")
            writer.close()
            await writer.wait_closed()
            break


async def main():
    pass



if __name__ == "__main__":
    #asyncio.run(main())
    loop = asyncio.get_event_loop()
    d = 2

    server = asyncio.start_server(
        host='localhost',
        port=8000,
        client_connected_cb=handler,
    )

    loop.create_task(server)
    loop.run_forever()