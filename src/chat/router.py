from fastapi import WebSocket, WebSocketDisconnect, APIRouter

from src.chat.manager import manager

router = APIRouter(
    prefix=f'/chat',
    tags=['Chat'],
)


@router.websocket("/ws/{client_name}")
async def websocket_endpoint(websocket: WebSocket,
                             client_name: str):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            # await manager.send_personal_message(f"You wrote: {data}", websocket)
            await manager.broadcast(f"{client_name}: {data}")
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        await manager.broadcast(f"{client_name} left the chat")
