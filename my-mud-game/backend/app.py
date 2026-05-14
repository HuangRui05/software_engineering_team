# backend/app.py
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from game_engine import game_engine   

app = FastAPI(title="MUD Game API", version="1.0")

# 允许跨域（开发环境）
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ----- 请求模型 -----
class JoinRequest(BaseModel):
    player_name: str

class MoveRequest(BaseModel):
    player_name: str
    direction: str

# ----- API 端点 -----
@app.get("/")
def root():
    return {"message": "MUD Game API is running"}

@app.post("/api/join")
def join_game(req: JoinRequest):
    player = game_engine.add_player(req.player_name)
    if not player:
        raise HTTPException(status_code=400, detail="玩家名称已存在")
    room_info = game_engine.get_room_info(req.player_name)
    return {"status": "ok", "room": room_info}

@app.post("/api/move")
def move_player(req: MoveRequest):
    result = game_engine.move_player(req.player_name, req.direction)
    if not result["success"]:
        raise HTTPException(status_code=400, detail=result["msg"])
    return result

@app.get("/api/status/{player_name}")
def get_status(player_name: str):
    info = game_engine.get_room_info(player_name)
    if not info:
        raise HTTPException(status_code=404, detail="玩家不存在")
    return info

@app.get("/api/players")
def list_players():
    return {"players": game_engine.list_players()}