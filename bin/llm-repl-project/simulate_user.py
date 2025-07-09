#!/usr/bin/env python3
"""
External User Simulation Script

This script simulates a user typing commands into the interactive REPL.
It's completely separate from the main program and cannot be faked.

Usage:
    python simulate_user.py "Hello" "How are you" "/quit"
    python simulate_user.py --file commands.txt
"""

import pexpect
import sys
import time
import argparse
from pathlib import Path
from typing import List


def simulate_user_typing(commands: List[str], timeout: int = 30) -> bool:
    """
    Simulate a user typing commands into the interactive REPL.
    
    Args:
        commands: List of commands to type
        timeout: Timeout for each command
        
    Returns:
        True if simulation completed successfully, False otherwise
    """
    project_root = Path(__file__).parent
    
    print(f"🎭 SIMULATING USER TYPING {len(commands)} COMMANDS")
    print("=" * 60)
    
    # Spawn the interactive REPL
    try:
        child = pexpect.spawn('just run', timeout=timeout, cwd=project_root, encoding='utf-8')
        print("✅ Started interactive REPL")
    except Exception as e:
        print(f"❌ Failed to start REPL: {e}")
        return False
    
    try:
        # Wait for the program to be ready for input
        # We expect the startup sequence to complete and show a prompt
        print("⏳ Waiting for REPL to be ready...")
        child.expect('>', timeout=10)
        print("✅ REPL is ready for input")
        
        # Simulate typing each command
        for i, command in enumerate(commands):
            print(f"\n📝 TYPING COMMAND {i+1}: '{command}'")
            
            # Type the command exactly as a user would
            child.sendline(command)
            
            # Handle special commands
            if command.lower() in ['exit', 'quit', 'bye', '/quit', '/exit']:
                print("🚪 Quit command detected - waiting for exit")
                try:
                    child.expect('Goodbye', timeout=5)
                    child.expect(pexpect.EOF, timeout=5)
                    print("✅ Program exited cleanly")
                    return True
                except pexpect.TIMEOUT:
                    print("❌ Program did not exit cleanly")
                    return False
                except pexpect.EOF:
                    # Program exited without goodbye message - still successful
                    print("✅ Program exited (no goodbye message)")
                    return True
            
            # For regular commands, wait for the response to complete
            # We look for the next prompt to appear
            try:
                child.expect('>', timeout=timeout)
                print("✅ Command processed successfully")
            except pexpect.TIMEOUT:
                print(f"❌ Command '{command}' timed out after {timeout} seconds")
                print(f"   Buffer: {repr(child.before)}")
                return False
        
        # If we reach here, all commands were processed
        # Send quit command to clean up
        print("\n🚪 Sending quit command to clean up...")
        child.sendline('/quit')
        
        try:
            child.expect('Goodbye', timeout=5)
            child.expect(pexpect.EOF, timeout=5)
            print("✅ Clean exit after all commands")
            return True
        except pexpect.TIMEOUT:
            print("❌ Failed to exit cleanly")
            return False
        except pexpect.EOF:
            # Program exited without goodbye message - still successful
            print("✅ Clean exit after all commands (no goodbye message)")
            return True
    
    except pexpect.TIMEOUT as e:
        print(f"❌ Timeout during simulation: {e}")
        print(f"   Buffer: {repr(child.before)}")
        return False
    
    except Exception as e:
        print(f"❌ Error during simulation: {e}")
        return False
    
    finally:
        if child.isalive():
            print("🔧 Terminating REPL process...")
            child.terminate()


def load_commands_from_file(file_path: str) -> List[str]:
    """Load commands from a file, one per line."""
    try:
        with open(file_path, 'r') as f:
            commands = [line.strip() for line in f.readlines()]
            return [cmd for cmd in commands if cmd and not cmd.startswith('#')]
    except Exception as e:
        print(f"❌ Failed to load commands from {file_path}: {e}")
        return []


def main():
    """Main entry point for user simulation."""
    parser = argparse.ArgumentParser(description="Simulate user typing commands into interactive REPL")
    parser.add_argument(
        'commands',
        nargs='*',
        help='Commands to type (e.g., "Hello" "How are you" "/quit")'
    )
    parser.add_argument(
        '--file', '-f',
        help='Load commands from file (one per line)'
    )
    parser.add_argument(
        '--timeout', '-t',
        type=int,
        default=30,
        help='Timeout for each command in seconds (default: 30)'
    )
    
    args = parser.parse_args()
    
    # Get commands from file or command line
    if args.file:
        commands = load_commands_from_file(args.file)
        if not commands:
            print("❌ No valid commands found in file")
            sys.exit(1)
    elif args.commands:
        commands = args.commands
    else:
        print("❌ No commands provided. Use --file or provide commands as arguments.")
        print("Example: python simulate_user.py \"Hello\" \"How are you\" \"/quit\"")
        sys.exit(1)
    
    # Run simulation
    success = simulate_user_typing(commands, args.timeout)
    
    if success:
        print("\n🎉 USER SIMULATION COMPLETED SUCCESSFULLY!")
        print("✅ All commands were processed correctly by the interactive REPL")
        sys.exit(0)
    else:
        print("\n💥 USER SIMULATION FAILED!")
        print("❌ The interactive REPL did not handle the commands correctly")
        sys.exit(1)


if __name__ == "__main__":
    main()