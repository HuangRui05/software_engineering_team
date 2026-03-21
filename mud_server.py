#!/usr/bin/env python3
"""
MUD Game Server - Multi-player Support
A text-based multi-user dungeon with network connectivity.
"""

import asyncio
from typing import Optional


# =============================================================================
# Game World Classes
# =============================================================================

class Room:
    """Represents a room in the game world."""
    
    def __init__(self, id: str, name: str, description: str):
        self.id = id
        self.name = name
        self.description = description
        self.exits = {}  # direction -> Room
        self.players = []  # List of Player objects in this room
    
    def add_exit(self, direction: str, room: 'Room'):
        """Add an exit in the given direction."""
        self.exits[direction] = room
    
    def get_exit(self, direction: str) -> 'Room | None':
        """Get the room in the given direction, or None if no exit."""
        return self.exits.get(direction)
    
    def describe(self) -> str:
        """Return a full description of the room."""
        exit_list = list(self.exits.keys())
        exits_str = ", ".join(exit_list) if exit_list else "none"
        
        desc = f"\n{'='*50}\n"
        desc += f"  {self.name}\n"
        desc += f"{'='*50}\n"
        desc += f"{self.description}\n\n"
        desc += f"Exits: {exits_str}\n"
        
        return desc
    
    def get_players_except(self, exclude_player: 'Player') -> list['Player']:
        """Get all players in this room except the specified one."""
        return [p for p in self.players if p != exclude_player]


class Player:
    """Represents a player in the game."""
    
    def __init__(self, name: str, room: Room, writer: asyncio.StreamWriter):
        self.name = name
        self.current_room = room
        self.writer = writer
        room.players.append(self)
    
    async def send(self, message: str):
        """Send a message to this player."""
        try:
            self.writer.write((message + "\n").encode('utf-8'))
            await self.writer.drain()
        except Exception:
            pass  # Player disconnected
    
    async def move(self, direction: str) -> tuple[bool, str]:
        """
        Attempt to move in the given direction.
        Returns (success, message) tuple.
        """
        direction = direction.lower()
        
        direction_map = {
            'n': 'north', 's': 'south', 'e': 'east', 'w': 'west',
            'north': 'north', 'south': 'south', 'east': 'east', 'west': 'west',
        }
        
        normalized = direction_map.get(direction)
        if not normalized:
            return False, f"I don't understand '{direction}'. Use: north, south, east, west (or n/s/e/w)."
        
        target_room = self.current_room.get_exit(normalized)
        
        if target_room is None:
            return False, f"You can't go {normalized} from here."
        
        # Leave current room
        self.current_room.players.remove(self)
        
        # Move to new room
        self.current_room = target_room
        self.current_room.players.append(self)
        
        return True, f"You go {normalized}."
    
    def look(self) -> str:
        """Return the current room's description with players."""
        desc = self.current_room.describe()
        
        other_players = [p for p in self.current_room.players if p != self]
        if other_players:
            names = ", ".join([p.name for p in other_players])
            desc += f"\nYou see other players here: {names}\n"
        else:
            desc += "\nYou are alone here.\n"
        
        return desc
    
    async def broadcast_to_room(self, message: str, exclude_self: bool = False):
        """Send a message to all players in the current room."""
        for player in self.current_room.players:
            if exclude_self and player == self:
                continue
            await player.send(message)


# =============================================================================
# World Creation
# =============================================================================

def create_world() -> dict[str, Room]:
    """Create the game world with connected rooms."""
    
    rooms = {
        "village_square": Room(
            "village_square",
            "Village Square",
            """You stand in the center of a small but bustling village.
A weathered stone fountain gurgles merrily in the middle.
Cobblestone paths radiate outward in four directions.
The smell of fresh bread drifts from a nearby bakery."""
        ),
        "old_temple": Room(
            "old_temple",
            "Old Temple",
            """You enter a sacred space that time has not been kind to.
Shafts of golden sunlight pierce through cracks in the ceiling.
The walls are covered in faded murals depicting heroes of old.
A broken altar stands at the far end."""
        ),
        "forest_path": Room(
            "forest_path",
            "Forest Path",
            """Tall oak and pine trees tower above you.
Birds sing melodiously from hidden perches.
The path is covered in a carpet of fallen needles.
Wildflowers dot the forest floor in splashes of color."""
        ),
        "dark_cave": Room(
            "dark_cave",
            "Dark Cave",
            """Cool air washes over you as you step into the cave's mouth.
Stalactites hang from the ceiling like stone teeth.
A cold draft emanates from deeper within.
Your eyes struggle to adjust to the dim light."""
        ),
    }
    
    # Connect rooms
    rooms["village_square"].add_exit("north", rooms["old_temple"])
    rooms["village_square"].add_exit("east", rooms["forest_path"])
    rooms["village_square"].add_exit("west", rooms["dark_cave"])
    
    rooms["old_temple"].add_exit("south", rooms["village_square"])
    rooms["forest_path"].add_exit("west", rooms["village_square"])
    rooms["dark_cave"].add_exit("east", rooms["village_square"])
    
    return rooms


# =============================================================================
# Game Server
# =============================================================================

class MUDServer:
    """Main MUD game server."""
    
    def __init__(self):
        self.world = create_world()
        self.players = []  # All connected players
    
    async def handle_client(self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter):
        """Handle a single client connection."""
        addr = writer.get_extra_info('peername')
        print(f"[+] New connection from {addr}")
        
        # Welcome message and get name
        await self.send_raw(writer, "=" * 50)
        await self.send_raw(writer, "       WELCOME TO THE MUD GAME")
        await self.send_raw(writer, "=" * 50)
        await self.send_raw(writer, "")
        
        player_name = await self.get_player_name(reader, writer)
        if not player_name:
            writer.close()
            await writer.wait_closed()
            return
        
        # Create player in starting room
        start_room = self.world["village_square"]
        player = Player(player_name, start_room, writer)
        self.players.append(player)
        
        await self.send_raw(writer, f"\nWelcome, {player.name}!")
        await self.send_raw(writer, "\nCommands: go <dir>, look, who, help, quit")
        await self.send_raw(writer, "=" * 50)
        
        # Announce to room
        await player.broadcast_to_room(
            f"\n*** {player.name} has entered the world. ***",
            exclude_self=True
        )
        
        # Show initial room
        await player.send(player.look())
        
        # Main game loop
        try:
            while True:
                data = await reader.readline()
                if not data:
                    break
                
                command = data.decode('utf-8').strip()
                if not command:
                    continue
                
                await self.process_command(player, command)
        except asyncio.CancelledError:
            pass
        except Exception as e:
            print(f"[!] Error with {player.name}: {e}")
        finally:
            await self.disconnect_player(player)
    
    async def send_raw(self, writer: asyncio.StreamWriter, message: str):
        """Send raw bytes to client."""
        try:
            writer.write((message + "\n").encode('utf-8'))
            await writer.drain()
        except Exception:
            pass
    
    async def get_player_name(self, reader: asyncio.StreamReader, 
                               writer: asyncio.StreamWriter) -> Optional[str]:
        """Prompt and validate player name."""
        while True:
            try:
                await self.send_raw(writer, "Enter your name: ")
                data = await reader.readline()
                
                if not data:
                    return None
                
                name = data.decode('utf-8').strip()
                
                if name and len(name) >= 2:
                    return name.capitalize()
                
                await self.send_raw(writer, "Please enter a name (at least 2 characters).")
                
            except Exception:
                return None
    
    async def process_command(self, player: Player, command: str):
        """Process a player command."""
        parts = command.lower().split()
        if not parts:
            return
        
        cmd = parts[0]
        args = parts[1:]
        
        if cmd in ("quit", "exit"):
            await player.send("\nThanks for playing! Goodbye.")
            player.writer.close()
            return
        
        elif cmd in ("go", "move"):
            if not args:
                await player.send("Go where? Use: go north, go south, go east, go west")
                return
            
            direction = args[0]
            success, message = await player.move(direction)
            await player.send(message)
            
            if success:
                await player.send(player.look())
                # Announce movement to old room
                await player.broadcast_to_room(
                    f">>> {player.name} has arrived.",
                    exclude_self=True
                )
        
        elif cmd in ("look", "l"):
            await player.send(player.look())
        
        elif cmd in ("who", "players"):
            await self.show_who(player)
        
        elif cmd in ("help", "h"):
            await self.show_help(player)
        
        else:
            await player.send(f"I don't understand '{cmd}'. Type 'help' for commands.")
    
    async def show_who(self, player: Player):
        """Show all players in the current room."""
        room = player.current_room
        other_players = [p for p in room.players if p != player]
        
        msg = f"\n{'='*40}\n"
        msg += f"Players in {room.name}:\n"
        msg += f"{'='*40}\n"
        
        if other_players:
            for p in other_players:
                msg += f"  - {p.name}\n"
            msg += f"\nTotal: {len(other_players)} player(s) besides you.\n"
        else:
            msg += "  (No other players here)\n"
        
        msg += f"{'='*40}\n"
        await player.send(msg)
    
    async def show_help(self, player: Player):
        """Show help message."""
        help_text = """
╔══════════════════════════════════════════════════════╗
║                  AVAILABLE COMMANDS                   ║
╠══════════════════════════════════════════════════════╣
║  MOVEMENT                                            ║
║    go <direction>  - Move in a direction             ║
║    n, s, e, w      - Shorthand for directions        ║
║                                                        ║
║  INFORMATION                                           ║
║    look (l)        - Examine your surroundings        ║
║    who             - Show players in current room     ║
║    help (h)        - Show this help message           ║
║                                                        ║
║  SYSTEM                                                ║
║    quit (exit)     - Leave the game                   ║
╚══════════════════════════════════════════════════════╝
"""
        await player.send(help_text)
    
    async def disconnect_player(self, player: Player):
        """Handle player disconnection."""
        print(f"[-] {player.name} disconnected")
        
        # Announce departure
        await player.broadcast_to_room(
            f"\n*** {player.name} has left the game. ***",
            exclude_self=True
        )
        
        # Remove from room and player list
        if player in player.current_room.players:
            player.current_room.players.remove(player)
        if player in self.players:
            self.players.remove(player)
        
        # Close connection
        try:
            player.writer.close()
            await player.writer.wait_closed()
        except Exception:
            pass
    
    async def run(self, host: str = "0.0.0.0", port: int = 4000):
        """Start the MUD server."""
        print("=" * 50)
        print("       MUD SERVER STARTING")
        print("=" * 50)
        print(f"Listening on {host}:{port}")
        print("Connect with: telnet localhost 4000")
        print("=" * 50)
        
        server = await asyncio.start_server(
            self.handle_client, host, port
        )
        
        async with server:
            await server.serve_forever()


# =============================================================================
# Entry Point
# =============================================================================

async def main():
    """Main entry point."""
    mud = MUDServer()
    try:
        await mud.run()
    except KeyboardInterrupt:
        print("\n\nServer shutting down...")


if __name__ == "__main__":
    asyncio.run(main())
