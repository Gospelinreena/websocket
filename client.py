import asyncio
import websockets
async def client():
    uri = "ws://localhost:8765"

    async with websockets.connect(uri) as websocket:
        username = input("Enter username: ")
        await websocket.send(username)

        async def send():
            loop = asyncio.get_event_loop()
            while True:
                msg = await loop.run_in_executor(None, input)
                await websocket.send(msg)

        async def receive():
            while True:
                try:
                    response = await websocket.recv()
                    print("\n" + response)
                except websockets.exceptions.ConnectionClosed:
                    print("Disconnected")
                    break

        await asyncio.gather(send(), receive())

        async def receive():
            while True:
                try:
                    response = await websocket.recv()
                    print("\n" + response)
                except websockets.exceptions.ConnectionClosed:
                    print("Disconnected")



        

asyncio.run(client())
