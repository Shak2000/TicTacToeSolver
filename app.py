from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from main import Game
from fastapi import Request

import json

game = Game()
app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def get_game_state():
    return {
        "board": game.board,
        "height": game.height,
        "width": game.width,
        "win": game.win,
        "player": game.player,
        "rem": game.rem,
        "misere": getattr(game, 'misere', False),
        "history": game.history,
        "winner": game.check_winner(),
    }


@app.get("/")
async def get_ui():
    return FileResponse("index.html")


@app.get("/styles.css")
async def get_styles():
    return FileResponse("styles.css")


@app.get("/script.js")
async def get_script():
    return FileResponse("script.js")


@app.post("/start")
async def start(height: int = 3, width: int = 3, win: int = 3, misere: bool = False):
    game.start(height, width, win, misere)
    return get_game_state()


@app.post("/move")
async def move(request: Request):
    data = await request.json()
    x = int(data.get("x"))
    y = int(data.get("y"))
    moved = game.move(x, y)
    if moved:
        game.rem -= 1
        winner = game.check_winner()
        if not winner and game.rem > 0:
            game.switch()
    return get_game_state()


@app.post("/undo")
async def undo():
    game.undo()
    return get_game_state()


@app.post("/restart")
async def restart():
    game.start(game.height, game.width, game.win, getattr(game, 'misere', False))
    return get_game_state()


@app.get("/state")
async def state():
    return get_game_state()


@app.get("/get_ai_move")
async def get_ai_move(depth: int):
    move = game.get_ai_move(depth)
    return {"move": move}


@app.get("/get_misere_ai_move")
async def get_misere_ai_move(depth: int):
    move = game.get_misere_ai_move(depth)
    return {"move": move}
