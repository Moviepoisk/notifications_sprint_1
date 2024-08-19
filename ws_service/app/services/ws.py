from fastapi.encoders import jsonable_encoder
from redis.asyncio import Redis

from fastapi import WebSocket


class WebsocketService:
    """Сервис рассылки сообщений по websocket для расчетного варианта."""

    TEXT_HELLO_PRESENT = "Представьтесь!"
    TEXT_HINT_TO_CHAT = 'Чтобы поговорить, напишите "<имя>: <сообщение>". Например: Ира: купи хлеб.'
    TEXT_HINT_TO_LOOK_UP = 'Посмотреть список участников можно командой "?"'

    def __init__(self, redis: Redis):
        self.redis = redis
        self.active_connections: dict[str, list[WebSocket]] = {}

    async def _welcome(self, websocket: WebSocket) -> str:
        await websocket.send_text(data=self.TEXT_HELLO_PRESENT)
        name = await websocket.receive_text()
        await websocket.send_text(data=self.TEXT_HINT_TO_CHAT)
        await websocket.send_text(data=self.TEXT_HINT_TO_LOOK_UP)
        return name

    async def connect(self, websocket: WebSocket) -> str:
        """Метод подключения websocket к сервису рассылки сообщений."""
        await websocket.accept()
        name = await self._welcome(websocket=websocket)
        if name in self.active_connections:
            self.active_connections[name].append(websocket)
        else:
            self.active_connections[name] = [websocket]
        return name

    def disconnect(self, websocket: WebSocket, key: str) -> None:
        """Метод отключения websocket от сервиса рассылки сообщений."""
        self.active_connections[key].remove(websocket)
        if not self.active_connections[key]:
            del self.active_connections[key]

    async def read_from_stream(self, key: str, websocket: WebSocket) -> None:
        """
        Метод подключения к очереди для чтения актуальных сообщений.

        :param key - ключ очереди.
        :param websocket - подключение на которое уходят сообщения.
        """
        while True:
            try:
                if resp := await self.redis.xread(streams={key: "$"}):
                    print(resp)
                    _, messages = resp[0]
                    for message in messages:
                        msg = jsonable_encoder(message[1])
                        await websocket.send_json(msg)
            except Exception:
                await websocket.close()
