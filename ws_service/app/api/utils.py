from app.services.ws import WebsocketService
from fastapi import WebSocket


async def read_from_stream(key: str, service: WebsocketService, websocket: WebSocket):
    """Метод задачи прослушивания очереди."""
    await service.read_from_stream(key=key, websocket=websocket)
