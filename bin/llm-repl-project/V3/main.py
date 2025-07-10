#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
LLM REPL V3 - Main Entry Point

Terminal-native LLM REPL designed for Arch + Sway integration.
Built with Textual framework for authentic terminal aesthetics.
"""

import argparse
import sys
from pathlib import Path

# Add V3 to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from app import LLMReplApp
from config.settings import get_config, list_configurations


def main():
    """Main entry point for LLM REPL V3"""
    parser = argparse.ArgumentParser(
        description="LLM REPL V3 - Terminal Interface",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python V3/main.py                     # Default debug config
  python V3/main.py --config fast      # Fast config
  python V3/main.py --config demo      # Demo config

Available Configurations:
""" + "\\n".join(f"  {name}: {desc}" for name, desc in list_configurations().items())
    )
    
    parser.add_argument(
        '--config', '-c',
        choices=['debug', 'fast', 'demo', 'test'],
        default='debug',
        help='Configuration preset to use (default: debug)'
    )
    
    parser.add_argument(
        '--version', '-v',
        action='version',
        version='LLM REPL V3.0.0 - Terminal Interface'
    )
    
    args = parser.parse_args()
    
    # Get configuration
    config = get_config(args.config)
    
    print("🚀 LLM REPL V3 - Terminal Interface")
    print("=" * 50)
    print(f"📋 Configuration: {config.name} - {config.description}")
    print(f"⚡ Cognition Delay: {config.cognition_delay}s per step")
    print(f"📏 Max Input Length: {config.max_input_length} characters")
    print()
    print("💡 V3 Features:")
    print("  ✅ Terminal-native TUI interface")
    print("  ✅ Sway window manager integration")
    print("  ✅ Terminal color scheme support")
    print("  ✅ Keyboard-first navigation")
    print("  ✅ Authentic terminal aesthetics")
    print("  ✅ All V2-5 functionality preserved")
    print()
    print("🎯 Keyboard Shortcuts:")
    print("  Enter: Send message")
    print("  Ctrl+L: Clear timeline")
    print("  Ctrl+C: Quit")
    print("  Escape: Cancel processing")
    print()
    
    try:
        # Create and run the application
        app = LLMReplApp(config_name=config.name)
        app.run()
        
    except KeyboardInterrupt:
        print("\\n👋 Goodbye!")
    except Exception as e:
        print(f"\\n❌ Error starting application: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()