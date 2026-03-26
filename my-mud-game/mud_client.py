#!/usr/bin/env python3
"""
Simple MUD Client for testing the MUD server.
Usage: python mud_client.py [username]
"""

import asyncio
import sys


async def mud_client(name: str = "Player"):
    """Connect to MUD server and interact."""
    
    try:
        reader, writer = await asyncio.open_connection('localhost', 4000)
    except ConnectionRefusedError:
        print("Error: Could not connect to MUD server.")
        print("Make sure the server is running: python mud_server.py")
        return
    except Exception as e:
        print(f"Error connecting: {e}")
        return
    
    print(f"\n✓ Connected to MUD server as '{name}'")
    print("=" * 40)
    
    # Read welcome and send name
    async def read_messages():
        """Read messages from server."""
        while True:
            try:
                data = await reader.readline()
                if not data:
                    print("\n[Disconnected from server]")
                    break
                
                msg = data.decode('utf-8').rstrip()
                print(msg)
                
                if "Enter your name:" in msg:
                    writer.write((name + "\n").encode('utf-8'))
                    await writer.drain()
            except asyncio.CancelledError:
                break
            except Exception as e:
                print(f"\n[Error: {e}]")
                break
    
    async def send_commands():
        """Send commands to server."""
        # Wait for connection to establish
        await asyncio.sleep(0.5)
        
        commands = [
            "look",
            "who",
            "go north",
            "look",
            "who",
            "help",
        ]
        
        for cmd in commands:
            await asyncio.sleep(1)
            print(f"\n[Sending: {cmd}]")
            writer.write((cmd + "\n").encode('utf-8'))
            await writer.drain()
        
        # Keep connection open briefly to receive final messages
        await asyncio.sleep(2)
        writer.write(b"quit\n")
        await writer.drain()
    
    try:
        # Run both tasks concurrently
        await asyncio.gather(
            read_messages(),
            send_commands()
        )
    finally:
        writer.close()
        try:
            await writer.wait_closed()
        except Exception:
            pass


async def main():
    name = sys.argv[1] if len(sys.argv) > 1 else "TestPlayer"
    await mud_client(name)


if __name__ == "__main__":
    asyncio.run(main())
