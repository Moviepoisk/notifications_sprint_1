from fastapi import FastAPI, status
from fastapi.testclient import TestClient
from fastapi.websockets import WebSocket

app = FastAPI()


@app.get("/")
async def read_main() -> dict:
    """
    Метод для тестирования get запроса на /.

    :return: Dict
    """
    return {"msg": "Hello World"}


@app.websocket("/ws")
async def websocket(websocket: WebSocket) -> None:
    """
    Метод тестирования подключения к websocket.

    :param websocket: Экземпляр класса WebSocket.
    :return: None (отправляет сообщение по websocket)
    """
    await websocket.accept()
    await websocket.send_json({"msg": "Hello WebSocket"})
    await websocket.close()


def test_read_main() -> None:
    """
    Тестирование get запроса на /.

    :return: None
    """
    client = TestClient(app)
    response = client.get("/")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"msg": "Hello World"}


def test_websocket() -> None:
    """
    Тестирование подключения к websocket.

    :return: None
    """
    client = TestClient(app)
    with client.websocket_connect("/ws") as websocket:
        data = websocket.receive_json()
        assert data == {"msg": "Hello WebSocket"}
