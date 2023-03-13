import datetime
import json
from collections import defaultdict
from dataclasses import dataclass, field
from itertools import combinations
from pathlib import Path
from typing import Dict, List, Optional

from fastapi import FastAPI, Request, WebSocket, WebSocketDisconnect
from fastapi.exceptions import HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles

app = FastAPI()


def get_winner(played):
    rock = "🪨"
    paper = "📰"
    scissors = "✂️"
    uid, move = list(played.keys()), list(played.values())
    for i in range(0, 2):
        j = (i + 1) % 2
        # same move
        if move[i] == move[j]:
            return None
        # rock breaks scissors, scissors cuts paper, paper covers rock.
        if (
            (move[i] == rock and move[j] == scissors)
            or (move[i] == scissors and move[j] == paper)
            or (move[i] == paper and move[j] == rock)
        ):
            return uid[i]


@dataclass
class GameState:
    players: Optional[List[str]] = field(default_factory=list)
    scores: Optional[Dict[str, int]] = field(default_factory=dict)
    sent: Optional[Dict[str, str]] = field(default_factory=dict)
    last_games: Optional[List] = field(default_factory=list)
    last_update: Optional[str] = None

    @property
    def is_sent(self):
        return {k: v is not None for k, v in self.sent.items()}

    def serialize(self):
        d = {
            "players": self.players,
            "last_update": self.last_update,
            "scores": self.scores,
            "is_sent": self.is_sent,
            "last_games": self.last_games,
        }
        if all([i for i in self.is_sent.values()]) and len(self.is_sent) > 1:
            # match random pairs and compare
            self.last_games = []
            for pair in list(combinations(self.players, 2)):
                played = {pair[i]: self.sent.get(pair[i]) for i in range(2)}
                winner = get_winner(played)
                g = {"players": pair, "played": played, "winner": winner}
                if g["winner"]:
                    self.scores[g["winner"]] += 1
                else:
                    g["winner"] = "draw"
                self.last_games.append(g)

            d["last_games"] = self.last_games
            self.sent = {k: None for k in self.players}
            d["is_sent"] = self.is_sent
        return d


game_states = defaultdict(lambda: GameState())


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
                if _data.get("f") == "add_user":
                    players = game_states[channel].players
                    if _data.get("user_id") not in players:
                        players.append(_data.get("user_id"))
                        game_states[channel].players = list(set(players))
                        game_states[channel].scores[_data.get("user_id")] = 0
                        game_states[channel].sent[_data.get("user_id")] = None
                if _data.get("f") == "send":
                    game_states[channel].sent[_data.get("user_id")] = _data.get("char")
                if False:
                    game_states[channel].scores[_data.get("user_id")] += 1
                game_states[channel].last_update = str(datetime.datetime.utcnow())
            except json.JSONDecodeError:
                pass
            data = game_states[channel].serialize()
            await ws_manager.broadcast(json.dumps(data), channel)
    except WebSocketDisconnect:
        ws_manager.disconnect(websocket, channel)


@app.get("/reset/{channel}")
async def reset_game(channel: str):
    game_states[channel].players = []
    return "ok"


@app.exception_handler(404)
async def redirect_all_requests_to_frontend(request: Request, exc: HTTPException):
    return HTMLResponse(open(Path(__file__).parent / "dist/index.html").read())


app.mount(
    "/assets",
    StaticFiles(directory=Path(__file__).parent / "dist/assets"),
    name="assets",
)
