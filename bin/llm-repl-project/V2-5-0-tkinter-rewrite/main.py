#!/usr/bin/env python3
"""
LLM REPL V3 - Modern Interface

Main entry point for the modern, professional LLM REPL interface.
Builds on V2's working functionality with modern styling and better organization.
"""

import argparse
import sys
from pathlib import Path

# Add V3 to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from ui.main_window import MainWindow
from config.settings import get_config, list_configurations


def main():
    """Main entry point for LLM REPL V3."""
    parser = argparse.ArgumentParser(
        description="LLM REPL V3 - Modern Interface",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python V3/main.py                     # Default debug config
  python V3/main.py --config fast      # Fast config
  python V3/main.py --theme dark       # Dark theme
  python V3/main.py --config demo --theme dark  # Demo with dark theme

Available Configurations:
""" + "\n".join(f"  {name}: {desc}" for name, desc in list_configurations().items())
    )
    
    parser.add_argument(
        '--config', '-c',
        choices=['debug', 'fast', 'demo', 'test'],
        default='debug',
        help='Configuration preset to use (default: debug)'
    )
    
    parser.add_argument(
        '--theme', '-t',
        choices=['light', 'dark'],
        default='light',
        help='UI theme to use (default: light)'
    )
    
    parser.add_argument(
        '--version', '-v',
        action='version',
        version='LLM REPL V3.0.0 - Modern Interface'
    )
    
    args = parser.parse_args()
    
    # Get configuration
    config = get_config(args.config)
    
    print("🚀 LLM REPL V3 - Modern Interface")
    print("=" * 50)
    print(f"📋 Configuration: {config.name} - {config.description}")
    print(f"🎨 Theme: {args.theme.title()}")
    print(f"⚡ Cognition Delay: {config.cognition_delay}s per step")
    print(f"📏 Max Input Length: {config.max_input_length} characters")
    print()
    print("💡 Key Improvements from V2:")
    print("  ✅ Modern, professional interface")
    print("  ✅ Better typography and spacing")
    print("  ✅ Improved color scheme and styling")
    print("  ✅ Enhanced accessibility features")
    print("  ✅ Menu bar with export and settings")
    print("  ✅ Keyboard shortcuts and help")
    print("  ✅ Better error handling and feedback")
    print()
    print("🎯 Preserved from V2:")
    print("  ✅ Block-based timeline architecture")
    print("  ✅ Cognitive processing pipeline")
    print("  ✅ Token tracking and transparency")
    print("  ✅ Expanding multiline input")
    print("  ✅ Reliable, bulletproof functionality")
    print()
    
    try:
        # Create and run the application
        app = MainWindow(config_name=config.name, theme_name=args.theme)
        
        # Configure cognition processor with config settings
        app.cognition_processor.configure_processing_delay(config.cognition_delay)
        
        # Run the application
        app.run()
        
    except KeyboardInterrupt:
        print("\n👋 Goodbye!")
    except Exception as e:
        print(f"\n❌ Error starting application: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()