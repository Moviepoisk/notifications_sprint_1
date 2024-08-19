import asyncio

from app.api.utils import read_from_stream
from app.core.dependencies import get_ws_service
from app.services.ws import WebsocketService
from fastapi import APIRouter, Depends, WebSocket, WebSocketDisconnect

router = APIRouter(prefix="/ws", tags=["ws"])


@router.websocket("/")
async def receiver(websocket: WebSocket, ws_service: WebsocketService = Depends(get_ws_service)) -> None:
    """Эндпоинт создания websocket для прослушивания сообщений."""
    name = await ws_service.connect(websocket=websocket)
    try:
        read = asyncio.create_task(read_from_stream(service=ws_service, websocket=websocket, key=name))
        await websocket.receive_text()
    except (WebSocketDisconnect, RuntimeError):
        ws_service.disconnect(websocket=websocket, key=name)
        read.cancel()
