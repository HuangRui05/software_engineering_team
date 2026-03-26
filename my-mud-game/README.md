# software_engineering_team

软件工程作业

## 团队基础信息

### 团队名称
薛定谔的 bug

### 团队口号
像猫一样敏捷 像呼噜声一样稳定

### 成员角色分配
| 姓名   | 学号          | Scrum 角色         |
|--------|---------------|--------------------|
| 黄瑞   | 9109223102    | Scrum Master (SM)  |
| 夏子航 | 9109223143    | 产品负责人 (PO)     |
| 汪嘉晨 | 9109223146    | 开发团队 (Dev Team) |

---

# MUD Game - Multi-player Setup

## Quick Start

### 1. Start the Server
```bash
python mud_server.py
```

Server will listen on **port 4000**.

### 2. Connect Clients

**Option A: Using Telnet**
```bash
telnet localhost 4000
```

**Option B: Using the test client**
```bash
python mud_client.py Alice
```

**Option C: Open multiple terminals**
```bash
# Terminal 1
telnet localhost 4000  # Enter name: Alice

# Terminal 2
telnet localhost 4000  # Enter name: Bob

# Terminal 3
telnet localhost 4000  # Enter name: Charlie
```

## Multi-player Features

### See Other Players
When you enter a room with other players:
```
=== Village Square ===
You stand in the center of a small but bustling village...

Exits: north, east, west

You see other players here: Alice, Bob
```

### Who Command
```
> who

========================================
Players in Village Square:
========================================
  - Alice
  - Bob

Total: 2 player(s) besides you.
========================================
```

### Player Notifications
When a player arrives:
```
>>> Alice has arrived.
```

When a player leaves:
```
*** Alice has left the game. ***
```

## Commands

| Command | Description |
|---------|-------------|
| `go <dir>` | Move (north/south/east/west) |
| `n/s/e/w` | Shorthand directions |
| `look` / `l` | Examine room |
| `who` | Show players in room |
| `help` / `h` | Show all commands |
| `quit` | Disconnect |

## World Map

```
              [Old Temple]
                   │
                   │ north/south
                   │
[Dark Cave] ──────┼────── [Forest Path]
   east/west      │        west/east
              [Village Square]
```

## Testing Multi-player

1. Start server: `python mud_server.py`
2. Open 3 terminal windows
3. Connect each with: `telnet localhost 4000`
4. Enter different names (Alice, Bob, Charlie)
5. Move around and use `who` to see others

## Architecture

```
┌─────────────┐     TCP:4000      ┌──────────────┐
│  Player 1   │ ◄───────────────► │              │
│  (Telnet)   │                   │  MUD Server  │
├─────────────┤                   │  (asyncio)   │
│  Player 2   │ ◄───────────────► │              │
│  (Telnet)   │                   └──────┬───────┘
├─────────────┤                          │
│  Player 3   │ ◄────────────────────────┤
│  (Telnet)   │                     [Rooms]
└─────────────┘                     [Players]
```

## Stop Server
Press `Ctrl+C` in the server terminal.
