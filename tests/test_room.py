def parse_room_info(room_data: dict) -> dict:
    """
    模拟游戏中解析房间信息的函数
    实际项目中，这部分是接口返回后前端/后端处理数据的逻辑
    """
    parsed = {
        "name": room_data.get("name", "").strip(),
        "description": room_data.get("description", "").strip(),
        "exits": room_data.get("exits", [])
    }
    return parsed

def test_parse_room_success():
    """测试：正常的房间数据，应该被正确解析"""
    raw_data = {
        "name": "中央广场",
        "description": "一个宽敞的广场，中心有一座喷泉",
        "exits": ["north", "south", "east", "west"]
    }
    room = parse_room_info(raw_data)
    assert room["name"] == "中央广场"
    assert "广场" in room["description"]
    assert len(room["exits"]) == 4
    assert "north" in room["exits"]

def test_parse_room_missing_exits():
    """测试：房间数据缺失出口信息，应该能正常处理，返回空列表"""
    raw_data = {
        "name": "神秘小屋",
        "description": "一间破旧的小屋"
    }
    room = parse_room_info(raw_data)
    assert room["name"] == "神秘小屋"
    assert room["exits"] == []
