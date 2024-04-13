from fastapi import (
    status,
    WebSocket,
    WebSocketDisconnect,

)
import sys
from app.server.database.collections import Collections
import app.server.database.core_data as model_service


class ConnectionManager:
    def __init__(self):
        self.active_connections: dict[str, WebSocket] = {}

    async def connect(self, websocket: WebSocket, client_id: str):
        # Do not allow connection with the same id
        if client_id in self.active_connections:
            await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
            sys.exit()
        self.active_connections[client_id] = websocket

        await self.handle_on_connect(websocket, client_id)

    def disconnect(self, client_id: str):
        if client_id in self.active_connections:
            del self.active_connections[client_id]

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast_all(self, message: str):
        for connection in self.active_connections.values():
            await connection.send_text(message)

    # Send a welcome message to the current client on connection
    async def handle_on_connect(self, websocket: WebSocket, client_id: str):
        welcome_message = f"Welcome, client #{client_id}! You are now connected."
        await websocket.send_text(welcome_message)


manager = ConnectionManager()


async def message_broadcast(websocket: WebSocket, client_id: str):
    await manager.connect(websocket, client_id)
    active_client_ids = list(manager.active_connections.keys())
    print(active_client_ids)
    try:
        while True:
            data = await websocket.receive_text()
            insert_data = {"senderName": client_id, "sentMessage": data}
            inserted_document = await model_service.create_one(Collections.MESSAGES, insert_data)
            await manager.send_personal_message(f"You wrote: {data}", websocket)
            await manager.broadcast_all(f"Client #{client_id} says: {data}")
    except WebSocketDisconnect:
        manager.disconnect(client_id)
        await manager.broadcast_all(f"Client #{client_id} left the chat")
