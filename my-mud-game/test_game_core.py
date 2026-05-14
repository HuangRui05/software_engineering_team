import pytest
from game_core import calculate_damage, trade_item

class TestCalculateDamage:
    def test_normal_damage(self):
        assert calculate_damage(10, 3) == 7
        assert calculate_damage(5, 5) == 1   # 至少1点伤害

    def test_damage_minimum(self):
        assert calculate_damage(3, 10) == 1   # 防御高于攻击
        assert calculate_damage(0, 100) == 1

    def test_critical_hit(self):
        assert calculate_damage(10, 3, crit=True) == 14  # (10-3)*2=14

class TestTradeItem:
    def test_successful_trade(self):
        success, new_gold, msg = trade_item(200, 50, 1)
        assert success is True
        assert new_gold == 150
        assert "成功" in msg

    def test_insufficient_gold(self):
        success, new_gold, msg = trade_item(30, 50, 1)
        assert success is False
        assert new_gold == 30
        assert "不足" in msg

    def test_zero_quantity(self):
        success, new_gold, msg = trade_item(100, 50, 0)
        assert success is False
        assert "无效" in msg

    def test_negative_quantity(self):
        success, new_gold, msg = trade_item(100, 50, -1)
        assert success is False
