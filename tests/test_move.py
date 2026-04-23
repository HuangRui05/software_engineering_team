def is_valid_move(current_room_exits: list, direction: str) -> bool:
    """
    模拟游戏中判断玩家移动是否合法的函数
    实际项目中，这部分逻辑是检查当前房间的出口，决定能否移动
    """
    valid_directions = ["north", "south", "east", "west"]
    # 先判断方向本身是否合法
    if direction not in valid_directions:
        return False
    # 再判断当前房间是否有这个出口
    return direction in current_room_exits

def test_move_valid():
    """测试：在中央广场（有所有出口）移动，应该合法"""
    current_exits = ["north", "south", "east", "west"]
    assert is_valid_move(current_exits, "north") is True
    assert is_valid_move(current_exits, "south") is True

def test_move_invalid_direction():
    """测试：输入不存在的方向（比如up），移动应该不合法"""
    current_exits = ["north", "south"]
    assert is_valid_move(current_exits, "up") is False

def test_move_blocked():
    """测试：当前房间没有该方向的出口，移动应该不合法"""
    current_exits = ["south"]  # 森林小径，只能往南走
    assert is_valid_move(current_exits, "north") is False
