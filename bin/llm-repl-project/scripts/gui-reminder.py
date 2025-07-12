#!/usr/bin/env python3
"""
GUI Application Reminder
Reminds agents about the GUI app ban when they mention running the app.
"""

import sys
import json

def main():
    try:
        # Read stdin for tool data
        data = json.load(sys.stdin)
        
        # Check if this is a tool that might involve running GUI apps
        tool_name = data.get('tool_name', '')
        tool_input = data.get('tool_input', {})
        
        gui_keywords = [
            'run the app', 'start the app', 'launch the app',
            'pdm run', 'python -m src.main', 'src.main',
            'run main.py', 'execute the gui', 'start gui',
            'run textual', 'textual run', 'textual dev',
            'take screenshot', 'capture screenshot', 'ctrl+r',
            'need to run', 'should run', 'let me run'
        ]
        
        # Check command content for GUI-related terms
        command = tool_input.get('command', '').lower()
        description = tool_input.get('description', '').lower()
        content = tool_input.get('content', '').lower()
        
        all_text = f"{command} {description} {content}"
        
        if any(keyword in all_text for keyword in gui_keywords):
            print("🚫 GUI APP REMINDER 🚫")
            print("")
            print("DETECTED: Mention of running GUI application")
            print("")
            print("❌ FORBIDDEN:")
            print("• Running python -m src.main")
            print("• Using pdm run src.main")
            print("• Any GUI app execution")
            print("• Taking new screenshots")
            print("")
            print("✅ CORRECT APPROACH:")
            print("• Use existing screenshots in debug_screenshots/")
            print("• Analyze code statically")
            print("• Review test outputs")
            print("• Read documentation files")
            print("")
            print("⚠️  VIOLATION: GUI apps break Claude Code interface!")
            
    except:
        # If anything fails, silently continue
        pass

if __name__ == '__main__':
    main()