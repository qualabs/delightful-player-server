import asyncio
import websockets

import ola_interface

from config import WEBSOCKET_IP, WEBSOCKET_PORT


async def server(ws: str, path: int):
    print('Client joined.')
    ola_interface.blink_all_lights()
    close_connection = False

    while True:
        try:
            json_colors = await ws.recv()
            color_list = ola_interface.parse_lights(json_colors)
            ola_interface.set_lights(color_list)
        except websockets.exceptions.ConnectionClosed as ex:
            print("Client disconnected. Do cleanup", ex)
            close_connection = True
            break
        except websockets.exceptions as ex:
            print("there was an error", ex)
            close_connection = True
            break

    if close_connection:
        await asyncio.sleep(1)
        await ws.close()
        print("connection closed")
        ola_interface.turn_off_all_lights()


print("Start execution.")
server = websockets.serve(server, WEBSOCKET_IP, WEBSOCKET_PORT)
asyncio.get_event_loop().run_until_complete(server)
asyncio.get_event_loop().run_forever()

