import asyncio
import websockets

async def server(ws:str, path:int):
    inp = input('client joined. greet it. \ntype ')
    await ws.send(inp)
    while true:
        message = await ws.recv()
        print(f'msg [{message}]')
        
print("start execution")
server = websockets.serve(server, 'localhost', 5678)

asyncio.get_event_loop().run_until_complete(server)
asyncio.get_event_loop().run_forever()

