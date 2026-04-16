# test_mud.py
import pytest
from mud_server import Room

def test_room_creation():
    """测试房间对象的创建和基本属性"""
    room = Room("start", "起始房间", "你在一个黑暗的房间里。")
    assert room.id == "start"
    assert room.name == "起始房间"
    assert room.description == "你在一个黑暗的房间里。"
    assert room.exits == {}
    assert room.players == []

def test_room_add_exit():
    """测试房间添加出口"""
    room1 = Room("1", "房间1", "")
    room2 = Room("2", "房间2", "")
    room1.add_exit("north", room2)
    assert room1.get_exit("north") == room2
    assert room1.get_exit("south") is None
