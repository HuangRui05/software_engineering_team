# backend/game_engine.py
from typing import Dict, List, Optional

class Room:
    """游戏房间"""
    def __init__(self, room_id: str, name: str, description: str):
        self.id = room_id
        self.name = name
        self.description = description
        self.exits: Dict[str, str] = {}   # direction -> room_id
        self.players: List[str] = []      # 玩家名称列表

    def add_exit(self, direction: str, room_id: str):
        self.exits[direction] = room_id

    def remove_player(self, player_name: str):
        if player_name in self.players:
            self.players.remove(player_name)

    def add_player(self, player_name: str):
        if player_name not in self.players:
            self.players.append(player_name)

class Player:
    """玩家"""
    def __init__(self, name: str):
        self.name = name
        self.current_room_id: str = "start"

class GameEngine:
    """游戏总控（单例）"""
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if self._initialized:
            return
        self._initialized = True
        self.rooms: Dict[str, Room] = {}
        self.players: Dict[str, Player] = {}
        self._init_world()

    def _init_world(self):
        # 创建房间
        start = Room("start", "中央广场", "一个宽敞的广场，中心有喷泉")
        forest = Room("forest", "森林小径", "树木茂密，阳光斑驳")
        lake = Room("lake", "湖边", "湖水清澈，微风吹过")

        # 设置双向出口
        start.add_exit("north", "forest")
        forest.add_exit("south", "start")
        forest.add_exit("east", "lake")
        lake.add_exit("west", "forest")

        self.rooms["start"] = start
        self.rooms["forest"] = forest
        self.rooms["lake"] = lake

    def add_player(self, name: str) -> Optional[Player]:
        if name in self.players:
            return None
        player = Player(name)
        self.players[name] = player
        start_room = self.rooms[player.current_room_id]
        start_room.add_player(name)
        return player

    def get_player(self, name: str) -> Optional[Player]:
        return self.players.get(name)

    def move_player(self, name: str, direction: str) -> Dict:
        player = self.players.get(name)
        if not player:
            return {"success": False, "msg": "玩家不存在"}

        current_room = self.rooms[player.current_room_id]
        if direction not in current_room.exits:
            return {"success": False, "msg": f"无法向 '{direction}' 移动"}

        new_room_id = current_room.exits[direction]
        current_room.remove_player(name)
        player.current_room_id = new_room_id
        new_room = self.rooms[new_room_id]
        new_room.add_player(name)

        return {
            "success": True,
            "room_id": new_room.id,
            "room_name": new_room.name,
            "room_desc": new_room.description,
            "exits": list(new_room.exits.keys()),
            "players": new_room.players
        }

    def get_room_info(self, name: str) -> Optional[Dict]:
        player = self.players.get(name)
        if not player:
            return None
        room = self.rooms[player.current_room_id]
        return {
            "room_id": room.id,
            "room_name": room.name,
            "room_desc": room.description,
            "exits": list(room.exits.keys()),
            "players": room.players
        }

    def list_players(self) -> List[str]:
        return list(self.players.keys())

# 全局单例实例
game_engine = GameEngine()