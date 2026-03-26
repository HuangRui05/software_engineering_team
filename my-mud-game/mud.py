#!/usr/bin/env python3
"""
MUD Game - MVP Room Movement System
A simple text-based multi-user dungeon game.
"""

class Room:
    """Represents a room in the game world."""
    
    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description
        self.exits = {}  # direction -> Room
    
    def add_exit(self, direction: str, room: 'Room'):
        """Add an exit in the given direction."""
        self.exits[direction] = room
    
    def get_exit(self, direction: str) -> 'Room | None':
        """Get the room in the given direction, or None if no exit."""
        return self.exits.get(direction)
    
    def describe(self) -> str:
        """Return a full description of the room."""
        exit_list = list(self.exits.keys())
        if exit_list:
            exits_str = ", ".join(exit_list)
        else:
            exits_str = "none"
        
        return f"""
=== {self.name} ===
{self.description}

Exits: {exits_str}
"""


class Player:
    """Represents a player in the game."""
    
    def __init__(self, name: str, start_room: Room):
        self.name = name
        self.current_room = start_room
    
    def move(self, direction: str) -> tuple[bool, str]:
        """
        Attempt to move in the given direction.
        Returns (success, message) tuple.
        """
        direction = direction.lower()
        
        # Map common abbreviations
        direction_map = {
            'n': 'north',
            's': 'south',
            'e': 'east',
            'w': 'west',
            'north': 'north',
            'south': 'south',
            'east': 'east',
            'west': 'west',
        }
        
        normalized = direction_map.get(direction)
        if not normalized:
            return False, f"I don't understand '{direction}'. Use: north, south, east, west (or n/s/e/w)."
        
        target_room = self.current_room.get_exit(normalized)
        
        if target_room is None:
            return False, f"You can't go {normalized} from here."
        
        self.current_room = target_room
        return True, f"You go {normalized}."
    
    def look(self) -> str:
        """Return the current room's description."""
        return self.current_room.describe()


def create_world() -> dict[str, Room]:
    """Create the game world with connected rooms."""

    # Create rooms with detailed descriptions
    village_square = Room(
        "Village Square",
        """You stand in the center of a small but bustling village.
A weathered stone fountain gurgles merrily in the middle, its water crystal clear.
Cobblestone paths radiate outward in four directions, worn smooth by countless footsteps.
The smell of fresh bread drifts from a nearby bakery, and villagers go about their daily chores.
To the NORTH, you see an ancient temple. To the EAST, a path leads into dense forest.
To the WEST, a dark cave mouth yawns invitingly."""
    )

    old_temple = Room(
        "Old Temple",
        """You enter a sacred space that time has not been kind to.
Shafts of golden sunlight pierce through cracks in the high ceiling, illuminating dancing dust motes.
The walls are covered in faded murals depicting heroes of old battling shadowy creatures.
A broken altar stands at the far end, still bearing the marks of ancient offerings.
The air feels heavy with forgotten prayers. The only exit is to the SOUTH, back to the village."""
    )

    forest_path = Room(
        "Forest Path",
        """Tall oak and pine trees tower above you, their canopy filtering sunlight into emerald patterns.
Birds sing melodiously from hidden perches, and a gentle breeze rustles the leaves.
The path is covered in a carpet of fallen needles, soft underfoot.
Squirrels chatter nervously as you pass. Wildflowers dot the forest floor in splashes of color.
The village lies to the WEST. Further east, the forest grows denser."""
    )

    dark_cave = Room(
        "Dark Cave",
        """Cool air washes over you as you step into the cave's mouth.
Stalactites hang from the ceiling like stone teeth, glistening with moisture.
The cave floor is uneven, scattered with rocks that crunch underfoot.
A cold draft emanates from deeper within, carrying the scent of damp earth.
Your eyes struggle to adjust to the dim light. The exit to the EAST leads back to sunlight."""
    )
    
    # Connect rooms
    # Village Square: center hub
    village_square.add_exit("north", old_temple)
    village_square.add_exit("east", forest_path)
    village_square.add_exit("west", dark_cave)
    
    # Old Temple: south leads back to village
    old_temple.add_exit("south", village_square)
    
    # Forest Path: west leads back to village
    forest_path.add_exit("west", village_square)
    
    # Dark Cave: east leads back to village
    dark_cave.add_exit("east", village_square)
    
    return {
        "village_square": village_square,
        "old_temple": old_temple,
        "forest_path": forest_path,
        "dark_cave": dark_cave,
    }


def parse_command(raw_input: str) -> tuple[str, list[str]]:
    """Parse player input into command and arguments."""
    parts = raw_input.strip().lower().split()
    if not parts:
        return "", []
    return parts[0], parts[1:]


def get_player_name() -> str:
    """Prompt the player to enter their name."""
    while True:
        try:
            name = input("Enter your name: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nGoodbye!")
            exit(0)
        
        if name and len(name) >= 2:
            return name.capitalize()
        print("Please enter a name (at least 2 characters).")


def main():
    """Main game loop."""

    # Initialize world
    world = create_world()

    # Welcome screen
    print("=" * 50)
    print("       WELCOME TO THE MUD GAME")
    print("=" * 50)
    print()

    # Get player name
    player_name = get_player_name()
    player = Player(player_name, world["village_square"])

    print(f"\nWelcome, {player.name}!")
    print("\nCommands:")
    print("  go <direction> - Move (north/south/east/west or n/s/e/w)")
    print("  look           - Examine your surroundings")
    print("  help           - Show all commands")
    print("  quit           - Exit the game")
    print("=" * 50)

    # Show initial room description
    print(player.look())
    
    # Main game loop
    while True:
        try:
            user_input = input("> ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nGoodbye!")
            break
        
        if not user_input:
            continue
        
        command, args = parse_command(user_input)
        
        if command == "quit" or command == "exit":
            print("Thanks for playing! Goodbye.")
            break
        
        elif command == "go":
            if not args:
                print("Go where? Use: go north, go south, go east, go west")
            else:
                direction = args[0]
                success, message = player.move(direction)
                print(message)
                if success:
                    print(player.look())
        
        elif command == "look" or command == "l":
            print(player.look())
        
        elif command == "help" or command == "h":
            print("""
╔══════════════════════════════════════════════════════╗
║                  AVAILABLE COMMANDS                   ║
╠══════════════════════════════════════════════════════╣
║  MOVEMENT                                            ║
║    go <direction>  - Move in a direction             ║
║    n, s, e, w      - Shorthand for directions        ║
║                                                        ║
║  INFORMATION                                           ║
║    look (l)        - Examine your surroundings        ║
║    help (h)        - Show this help message           ║
║                                                        ║
║  SYSTEM                                                ║
║    quit (exit)     - Leave the game                   ║
╚══════════════════════════════════════════════════════╝
""")

        else:
            print(f"I don't understand '{command}'. Type 'help' for commands.")


if __name__ == "__main__":
    main()
