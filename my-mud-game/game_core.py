# game_core.py
"""模拟 MUD 游戏的核心战斗与交易逻辑"""

def calculate_damage(attacker_power: int, defender_defense: int, crit: bool = False) -> int:
    """
    计算攻击造成的伤害。
    伤害公式：基础伤害 = max(1, attacker_power - defender_defense)
    若暴击(crit)则伤害翻倍。
    """
    base = max(1, attacker_power - defender_defense)
    return base * 2 if crit else base

def trade_item(buyer_gold: int, seller_price: int, buyer_item_count: int = 1) -> tuple:
    """
    交易物品。
    返回值: (success: bool, new_buyer_gold: int, message: str)
    """
    if buyer_gold < seller_price:
        return (False, buyer_gold, "金币不足")
    if buyer_item_count <= 0:
        return (False, buyer_gold, "购买数量无效")
    new_gold = buyer_gold - seller_price
    return (True, new_gold, f"购买成功，花费 {seller_price} 金币")