#!/usr/bin/env python3
"""zmdfmt: Zack's source-preserving Markdown formatter.

Architecture:
    input markdown
      -> protect byte-sensitive regions (wikilinks, math, code fences)
      -> segment into prose zones and opaque zones
      -> run Flowmark on approved prose zones
      -> run tiny style passes with fixture coverage
      -> restore protected regions byte-for-byte
      -> ensure final newline
"""

import sys
from pathlib import Path

from zmdfmt.passes.final_newline import ensure_final_newline
from zmdfmt.protect.math import protect_math, restore_math
from zmdfmt.protect.wikilinks import protect_wikilinks, restore_wikilinks


def format_text(src: str) -> str:
    """Format a Markdown source string, preserving unknown syntax."""
    text = src

    # Protect byte-sensitive regions before any tool touches them.
    text = protect_wikilinks(text)
    text = protect_math(text)

    # TODO: segment prose zones, run Flowmark, apply style passes

    # Restore protected regions byte-for-byte.
    text = restore_wikilinks(text)
    text = restore_math(text)

    # Trivial byte cleanup (allowed per spec).
    text = ensure_final_newline(text)

    return text


def main():
    if len(sys.argv) < 2:
        text = sys.stdin.read()
        output = format_text(text)
        sys.stdout.write(output)
        return

    input_path = Path(sys.argv[1])
    src = input_path.read_text()
    output = format_text(src)

    if "--check" in sys.argv:
        if output != src:
            sys.exit(1)
        return

    if "--stdout" in sys.argv:
        sys.stdout.write(output)
        return

    input_path.write_text(output)


if __name__ == "__main__":
    main()
