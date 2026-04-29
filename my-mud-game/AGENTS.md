# AGENTS.md – MUD 文字地牢游戏

## 项目概述
- 基于 Python asyncio 的多人在线文字游戏（MUD）。
- 核心模块：`mud_server.py`（主服务器）、`mud_client.py`（命令行客户端）、`game_core.py`（战斗/交易逻辑）。

## 目录结构


my-mud-game/
├── .github/workflows/ # CI 流水线（ci.yml）
├── docs/ # OpenAPI 契约（openapi.yaml）
├── mock-client/ # Mock 前端页面（本地演示用）
├── game_core.py # 核心业务函数（无状态，纯计算）
├── mud_server.py # 网络服务器与游戏循环
├── mud_client.py # 客户端交互
├── test_game_core.py # 单元测试（pytest）
├── test_mud.py # 原有测试（Room/Player）
├── AGENTS.md # 本文档
└── README.md


## 核心模块职责
- `mud_server.MUDServer` – 监听连接，接收指令，协调玩家与房间。
- `mud_server.Room` – 房间管理，出口映射，玩家列表。
- `mud_server.Player` – 玩家状态，移动逻辑，消息发送。
- `game_core` – 战斗伤害计算、物品交易（纯函数，易于测试）。

## 编码规范
- 缩进：4 空格
- 行长度 ≤ 120
- 所有函数必须包含类型注解
- 公共函数必须有 docstring
- 异步函数命名以 `_async` 结尾

## 禁止操作
- ❌ 在 `game_core.py` 中引入网络 I/O 或异步操作
- ❌ 在测试中使用 `time.sleep()` 代替 `asyncio` 等待
- ❌ 硬编码玩家数据（未来应使用 SQLite）
- ❌ 直接修改 `Room.players` 列表（必须通过 `Player.move` 方法）