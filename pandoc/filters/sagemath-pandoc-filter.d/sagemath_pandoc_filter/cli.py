#!/usr/bin/env python3
"""Command-line interface for the Sage Filter."""

import argparse
import sys
from typing import Optional

def main(args: Optional[list] = None) -> int:
    """Run the Sage Filter from the command line.
    
    Args:
        args: Command line arguments (defaults to sys.argv[1:])
        
    Returns:
        int: Exit code (0 for success, non-zero for errors)
    """
    parser = argparse.ArgumentParser(
        description='Process Sage code in Markdown documents with Pandoc.'
    )
    
    parser.add_argument(
        '--version',
        action='version',
        version='%(prog)s 0.1.0'
    )
    
    # Parse known args to avoid conflict with pandoc-filter
    args, _ = parser.parse_known_args(args)
    
    try:
        from .filter import main as filter_main
        return filter_main()
    except ImportError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1

if __name__ == '__main__':
    sys.exit(main())
