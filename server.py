import asyncio
import websockets
connected_clients = {}

async def server(websocket):
    username = None
    try:
        username = await websocket.recv()

        if username in connected_clients:
            await websocket.send("Username already taken. Try another.")
            return

        connected_clients[username] = websocket

        print(f"{username} connected")
        print("Total clients:", len(connected_clients))

        await asyncio.gather(
            *[
                client.send(f"{username} joined")
                for client in connected_clients.values()
            ]
        )

        async for message in websocket:
            print(f"{username}: {message}")

            await asyncio.gather(
                *[
                    client.send(f"{username}: {message}")
                    for client in connected_clients.values()
                ]
            )

    except websockets.exceptions.ConnectionClosed:
        print(f"{username} disconnected")

    finally:
        if username and username in connected_clients:
            del connected_clients[username]

            print(f"{username} removed")
            print("Total clients:", len(connected_clients))

            if connected_clients:
                await asyncio.gather(
                    *[
                        client.send(f"{username} left")
                        for client in connected_clients.values()
                    ]
                )
async def main():
    async with websockets.serve(server, "localhost", 8765):
        print("Server started on ws://localhost:8765")
        await asyncio.Future() 

asyncio.run(main())