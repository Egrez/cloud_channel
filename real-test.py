
# chat_client.py

import asyncio
import websockets
import aioconsole

import websocket

import requests
import json



async def received_message_handler(websocket):
    while True:
        message = await websocket.recv()
        await aioconsole.aprint(message)


async def sent_message_handler(websocket):
    while True:
        message = json.dumps({"tds" : 1, "pH" : 2, "cond" : 3,})
        await asyncio.sleep(5)
        await websocket.send(message)


async def main():
    uri = "wss://web-production-859c.up.railway.app/ws/sensor"

    session = requests.Session()

    username = 'serge'
    password = '123'

    post_data = {'username': username, 'password' : password}

    session.post('https://web-production-859c.up.railway.app/signin', data=post_data)

    cookies = session.cookies.get_dict()

    print(uri)

    print(cookies)

    async with websockets.connect(uri, extra_headers=cookies) as websocket:
        await asyncio.gather(
            received_message_handler(websocket),
            sent_message_handler(websocket)
        )

asyncio.get_event_loop().run_until_complete(main())
asyncio.get_event_loop.run_forever()