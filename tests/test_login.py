def test_login_right():
    user = "admin"
    pwd = "123456"
    assert user == "admin"
    assert pwd == "123456"

def test_login_error():
    wrong_pwd = "654321"
    assert wrong_pwd != "123456"
