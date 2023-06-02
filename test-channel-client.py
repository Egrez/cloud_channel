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
    uri = "ws://localhost:8000/ws/sensor"

    session = requests.Session()

    username = 'serge'
    password = '123'

    post_data = {'username': username, 'password' : password}

    session.post('http://localhost:8000/signin', data=post_data)

    cookies = session.cookies.get_dict()

    print(cookies)

    # sign in POST request


    async with websockets.connect(uri, extra_headers=cookies) as websocket:
        await asyncio.gather(
            received_message_handler(websocket),
            sent_message_handler(websocket)
        )

asyncio.get_event_loop().run_until_complete(main())
asyncio.get_event_loop.run_forever()

# from time import sleep

# def on_open(ws):
#     print("connection established")
#     while True:
#         ws.send(json.dumps({"message" : "ligma"}))
#         print("gumagana ba to")
#         sleep(5)


# # Callback for handling WebSocket message event
# def on_message(ws, message):
#     while True:
#         print(message)

# # Callback for handling WebSocket error event
# def on_error(ws, error):
#     print("Error encountered: {}".format(error))

# # Callback for handling WebSocket close event
# def on_close(ws):
#     print("WebSocket connection closed.")

# session = requests.Session()

# username = 'serge'
# password = '123'

# post_data = {'username': username, 'password' : password}

# session.post('http://localhost:8000/signin', data=post_data)

# cookies = session.cookies.get_dict()

# print(cookies)
# print("; ".join(["%s=%s" %(i, j) for i, j in cookies.items()]))

# https://stackoverflow.com/questions/58866803/create-websocket-connection-from-requests-session-in-python
# ws = websocket.WebSocketApp(
#         'ws://localhost:8000/ws/sensor',
#         cookie="; ".join(["%s=%s" %(i, j) for i, j in cookies.items()]), 
#         on_open=on_open, 
#         on_message=on_message, 
#         on_error=on_error, 
#         on_close=on_close
#     )
# ws.run_forever()