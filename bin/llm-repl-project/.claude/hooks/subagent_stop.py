#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "python-dotenv",
# ]
# ///

"""
SubagentStop Hook - Subagent Completion Control

CLAUDE COMMUNICATION METHODS:
================================================================================
This hook can directly communicate with Claude subagents using these methods:

1. EXIT CODE 2 + stderr:
   - Blocks subagent from stopping (forces continuation)
   - stderr content is automatically fed to the SUBAGENT as instructions
   - Subagent receives the message and must continue working
   - Example: sys.exit(2) with print("Continue: task incomplete", file=sys.stderr)

2. JSON OUTPUT + EXIT CODE 0:
   Advanced control via stdout JSON:
   
   a) Decision Control:
      {"decision": "block", "reason": "explanation"}
      - Prevents subagent from stopping
      - Reason tells subagent how to proceed
      - Subagent receives reason and continues working
      
   b) Session Control:
      {"continue": false, "stopReason": "reason"}
      - Stops subagent entirely, reason shown to user (NOT subagent)

3. NO COMMUNICATION (Exit Code 0, no stderr):
   - Allows normal subagent completion
   - Only logging and TTS occurs

CURRENT IMPLEMENTATION: Uses method #3 (no communication) - allows normal completion
NOTE: Subagents are Task tool invocations that can be controlled independently
================================================================================
"""

import argparse
import json
import os
import sys
import subprocess
from pathlib import Path
from datetime import datetime
from utils.common_logger import create_logger

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass  # dotenv is optional


def get_tts_script_path():
    """
    Determine which TTS script to use based on available API keys.
    Priority order: ElevenLabs > OpenAI > pyttsx3
    """
    # Get current script directory and construct utils/tts path
    script_dir = Path(__file__).parent
    tts_dir = script_dir / "utils" / "tts"
    
    # Check for ElevenLabs API key (highest priority)
    if os.getenv('ELEVENLABS_API_KEY'):
        elevenlabs_script = tts_dir / "elevenlabs_tts.py"
        if elevenlabs_script.exists():
            return str(elevenlabs_script)
    
    # Check for OpenAI API key (second priority)
    if os.getenv('OPENAI_API_KEY'):
        openai_script = tts_dir / "openai_tts.py"
        if openai_script.exists():
            return str(openai_script)
    
    # Fall back to pyttsx3 (no API key required)
    pyttsx3_script = tts_dir / "pyttsx3_tts.py"
    if pyttsx3_script.exists():
        return str(pyttsx3_script)
    
    return None


def announce_subagent_completion():
    """Announce subagent completion using the best available TTS service."""
    try:
        tts_script = get_tts_script_path()
        if not tts_script:
            return  # No TTS scripts available
        
        # Use fixed message for subagent completion
        completion_message = "Subagent Complete"
        
        # Call the TTS script with the completion message
        subprocess.run([
            "uv", "run", tts_script, completion_message
        ], 
        capture_output=True,  # Suppress output
        timeout=10  # 10-second timeout
        )
        
    except (subprocess.TimeoutExpired, subprocess.SubprocessError, FileNotFoundError):
        # Fail silently if TTS encounters issues
        pass
    except Exception:
        # Fail silently for any other errors
        pass


def main():
    logger = create_logger('subagent_stop')
    
    try:
        # Parse command line arguments
        parser = argparse.ArgumentParser()
        parser.add_argument('--chat', action='store_true', help='Copy transcript to chat.json')
        args = parser.parse_args()
        
        # Read JSON input from stdin
        input_data = json.load(sys.stdin)

        # Extract required fields
        session_id = input_data.get("session_id", "")
        stop_hook_active = input_data.get("stop_hook_active", False)

        # Log the event
        logger.log_event({**input_data, 'chat_export_enabled': args.chat})
        
        # Handle --chat switch (same as stop.py)
        if args.chat and 'transcript_path' in input_data:
            transcript_path = input_data['transcript_path']
            if os.path.exists(transcript_path):
                # Read .jsonl file and convert to JSON array
                chat_data = []
                try:
                    with open(transcript_path, 'r') as f:
                        for line in f:
                            line = line.strip()
                            if line:
                                try:
                                    chat_data.append(json.loads(line))
                                except json.JSONDecodeError:
                                    pass  # Skip invalid lines
                    
                    # Write to logs/chat.json
                    log_dir = logger.log_dir
                    chat_file = log_dir / 'chat.json'
                    with open(chat_file, 'w') as f:
                        json.dump(chat_data, f, indent=2)
                except Exception as e:
                    logger.log_error(f"Failed to export chat transcript: {str(e)}", {"transcript_path": transcript_path})

        # Announce subagent completion via TTS
        announce_subagent_completion()

        sys.exit(0)

    except json.JSONDecodeError:
        logger.log_error("JSON decode error", {"raw_input": "invalid"})
        sys.exit(0)
    except Exception as e:
        logger.log_error(f"Unexpected error: {str(e)}", input_data if 'input_data' in locals() else {})
        sys.exit(0)


if __name__ == "__main__":
    main()