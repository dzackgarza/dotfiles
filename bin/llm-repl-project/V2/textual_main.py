#!/usr/bin/env python3
"""
Textual Main Entry Point - Simple launcher for the new Textual interface

USAGE:
    python textual_main.py                    # Run with default config
    python textual_main.py --config fast     # Run with specific config
    python textual_main.py --simple          # Run simple version without LLM integration
"""

import asyncio
import argparse
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))


async def run_simple_app():
    """Run the simple Textual app without LLM integration."""
    from textual_app import main as simple_main
    await simple_main()


async def run_enhanced_app(config_name: str):
    """Run the enhanced Textual app with full LLM integration."""
    try:
        from textual_llm_integration import EnhancedLLMREPLApp
        app = EnhancedLLMREPLApp(config_name=config_name)
        await app.run_async()
    except ImportError as e:
        print(f"Could not import LLM integration: {e}")
        print("Falling back to simple app...")
        await run_simple_app()


def main():
    """Main entry point with argument parsing."""
    parser = argparse.ArgumentParser(
        description="LLM REPL with Textual Interface",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python textual_main.py                    # Default config
  python textual_main.py --config fast     # Fast config
  python textual_main.py --simple          # Simple version
        """
    )
    
    parser.add_argument(
        '--config', '-c',
        choices=['debug', 'mixed', 'fast', 'test'],
        default='debug',
        help='Configuration to use (default: debug)'
    )
    
    parser.add_argument(
        '--simple', '-s',
        action='store_true',
        help='Run simple version without LLM integration'
    )
    
    parser.add_argument(
        '--version', '-v',
        action='version',
        version='LLM REPL Textual v1.0.0'
    )
    
    args = parser.parse_args()
    
    print("🚀 Starting LLM REPL with Textual Interface...")
    print(f"📋 Configuration: {args.config}")
    print(f"🔧 Mode: {'Simple' if args.simple else 'Enhanced'}")
    print()
    
    try:
        if args.simple:
            asyncio.run(run_simple_app())
        else:
            asyncio.run(run_enhanced_app(args.config))
    except KeyboardInterrupt:
        print("\n👋 Goodbye!")
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()