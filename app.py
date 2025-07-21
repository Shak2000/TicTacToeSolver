from fastapi import FastAPI
from fastapi.responses import FileResponse
from pydantic import BaseModel
from main import Game

game = Game()
app = FastAPI()

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
async def start(height: int = 3, width: int = 3, win: int = 3):
    game.start(height, width, win)


@app.post("/switch")
async def switch():
    game.switch()


@app.post("/move")
async def move(x, y):
    return game.move(x, y)


@app.post("/undo")
async def undo():
    return game.undo()


@app.post("/check_winner")
async def check_winner():
    return game.check_winner()


@app.get("/get_valid_moves")
async def get_valid_moves():
    return game.get_valid_moves()


@app.get("/evaluate")
async def evaluate(player):
    return game.evaluate(player)


@app.get("/minimax")
async def minimax(depth, alpha, beta, player, root_player):
    return game.minimax(depth, alpha, beta, player, root_player)


@app.get("/get_ai_move")
async def get_ai_move(depth):
    return game.get_ai_move(depth)
