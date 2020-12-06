import asyncio
import datetime
import random
import time
from threading import Thread

import websockets


async def time_handler(websocket, path):
    while True:
        now = datetime.datetime.utcnow().isoformat() + "Z"
        await websocket.send(now)
        await asyncio.sleep(random.random() * 3)


def start_new_server():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    start_server = websockets.serve(time_handler, "192.168.1.52", 4321)
    asyncio.get_event_loop().run_until_complete(start_server)
    asyncio.get_event_loop().run_forever()


if __name__ == '__main__':
    # start_new_server()
    thread = Thread(target=start_new_server)
    thread.start()
    while True:
        print(datetime.datetime.utcnow())
        time.sleep(5)
    # thread.join()