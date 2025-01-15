import asyncio
import telegram


SEND_TO_TELEGRAM = False
TELEGRAM_TOKEN ='7750977038:AAFjVHscmTJb-0IKs1YPDenHDCnXe1rt1p4'
TELEGRAM_CHAT_ID ='-1002376523103'


async def send_telegram_message(message):
    try:
        bot = telegram.Bot(token=TELEGRAM_TOKEN)
        chat_id = TELEGRAM_CHAT_ID
        await bot.send_message(chat_id=chat_id, text=message)
        return 200
    except Exception as ex:
        await asyncio.sleep(0)
        return ex


async def handler(reader, writer):
    serve, escape = True, False
    lines = []

    while serve:
        raw_line = await reader.readline()
        decoded_line = raw_line.decode('utf-8').strip('\r\n')
        if decoded_line:
            lines.append(decoded_line)
        else:
            if lines:
                if SEND_TO_TELEGRAM:
                    answer = await send_telegram_message(message=lines)
                    print(answer)
                [print(line) for line in lines]
                print()

                response_body = '\r\n'.join(lines)
                response_headers = [
                    'HTTP/1.1 200 OK',
                    'Content-Type: text/plain; charset=utf-8',
                    f'Content-Length: {len(response_body)+15}',
                    'Connection: close',
                    '',
                    'YOUR REQUEST:',
                    response_body,
                ]
                lines = []

                response = '\r\n'.join(response_headers)

                writer.write(response.encode('utf-8'))
                break


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