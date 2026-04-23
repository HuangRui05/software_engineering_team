# 模拟你们游戏的登录校验逻辑
def validate_login(username: str, password: str) -> bool:
    """
    模拟游戏的登录校验函数
    实际项目中这部分逻辑在后端/前端都有，这里是为了测试
    """
    valid_users = {
        "player1": "password123",
        "admin": "admin123"
    }
    return username in valid_users and valid_users[username] == password

def test_login_success():
    """测试：正确的用户名和密码，应该登录成功"""
    assert validate_login("player1", "password123") is True
    assert validate_login("admin", "admin123") is True

def test_login_wrong_password():
    """测试：用户名正确但密码错误，应该登录失败"""
    assert validate_login("player1", "wrongpass") is False

def test_login_user_not_exist():
    """测试：不存在的用户名，应该登录失败"""
    assert validate_login("hacker", "123456") is False
