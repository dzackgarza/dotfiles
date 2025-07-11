#!/usr/bin/env python3
"""Simple script to print dimmed text output for build scripts."""
import sys

def dim_print(text):
    """Print text in dim gray color using Rich if available, otherwise plain."""
    try:
        from rich.console import Console
        console = Console()
        console.print(text, style="dim")
    except ImportError:
        # Fallback to plain print if Rich not available
        print(text)

if __name__ == "__main__":
    if len(sys.argv) > 1:
        dim_print(" ".join(sys.argv[1:]))
    else:
        dim_print("")