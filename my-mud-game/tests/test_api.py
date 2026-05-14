import pytest
from fastapi.testclient import TestClient
from backend.app import app

client = TestClient(app)

def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "MUD Game API is running"}

def test_join_and_move():
    player_name = "tester_integration"
    # 加入
    join_resp = client.post("/api/join", json={"player_name": player_name})
    assert join_resp.status_code == 200
    data = join_resp.json()
    assert data["status"] == "ok"
    # 获取状态
    status_resp = client.get(f"/api/status/{player_name}")
    assert status_resp.status_code == 200
    room_info = status_resp.json()
    assert "exits" in room_info
    # 移动
    move_resp = client.post("/api/move", json={"player_name": player_name, "direction": "north"})
    assert move_resp.status_code == 200
    move_data = move_resp.json()
    assert move_data["success"] is True
    assert move_data["room_name"] in ["森林小径", "Forest"]
    