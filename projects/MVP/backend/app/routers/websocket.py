import json
from fastapi import WebSocket
from fastapi.websockets import WebSocketDisconnect


user_connections = {}

async def broadcast_message(user_id: int, message: dict):
    if user_id in user_connections:
        for connection in user_connections[user_id]:
            await connection.send_text(json.dumps(message))

async def user_websocket(websocket: WebSocket, user_id: int):
    await websocket.accept()
    if user_id not in user_connections:
        user_connections[user_id] = []
    user_connections[user_id].append(websocket)

    print("user connections: ", user_connections)

    try:
        while True:
            data = await websocket.receive_text() 
            message = json.loads(data)
            await broadcast_message(user_id, message)
    except WebSocketDisconnect:
        user_connections[user_id].remove(websocket)
        print(f"User {user_id} disconnected.")
        
