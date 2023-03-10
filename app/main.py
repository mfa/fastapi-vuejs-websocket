import json
from collections import defaultdict
from pathlib import Path
from typing import Dict

from fastapi import FastAPI, Request, WebSocket, WebSocketDisconnect
from fastapi.exceptions import HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles

app = FastAPI()


class WebsocketConnectionManager:
    def __init__(self):
        self.active_connections: Dict[WebSocket] = defaultdict(list)

    async def connect(self, websocket: WebSocket, channel: str):
        await websocket.accept()
        self.active_connections[channel].append(websocket)

    def disconnect(self, websocket: WebSocket, channel: str):
        if websocket in self.active_connections[channel]:
            self.active_connections[channel].remove(websocket)

    async def broadcast(self, message: str, channel: str):
        for connection in self.active_connections.get(channel, []):
            await connection.send_text(message)


ws_manager = WebsocketConnectionManager()


@app.websocket("/ws/{channel}")
async def websocket_endpoint(
    channel: str,
    websocket: WebSocket,
):
    await ws_manager.connect(websocket, channel)
    try:
        while True:
            data = await websocket.receive_text()
            try:
                _data = json.loads(data)
                if _data.get("f") == "add":
                    data = str(sum(_data.get("params")))
            except json.JSONDecodeError:
                pass
            await ws_manager.broadcast(data, channel)
    except WebSocketDisconnect:
        ws_manager.disconnect(websocket, channel)


@app.exception_handler(404)
async def redirect_all_requests_to_frontend(request: Request, exc: HTTPException):
    return HTMLResponse(open(Path(__file__).parent / "dist/index.html").read())


app.mount(
    "/assets",
    StaticFiles(directory=Path(__file__).parent / "dist/assets"),
    name="assets",
)
