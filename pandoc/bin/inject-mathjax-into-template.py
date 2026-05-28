#!/usr/bin/env python3
"""Inject compact MathJax macros JSON into the pandoc preview template.

Usage:
    inject-mathjax-into-template.py <template_path> <macros_json_path>

Reads the macros JSON, compacts it to a single line, and replaces the
MATHJAX_MACROS_JSON placeholder in the template with the inline macros.
"""

import json
import sys
from pathlib import Path


def main() -> None:
    if len(sys.argv) != 3:
        print(
            f"Usage: {sys.argv[0]} <template_path> <macros_json_path>", file=sys.stderr
        )
        sys.exit(1)

    template_path = Path(sys.argv[1])
    macros_json_path = Path(sys.argv[2])

    if not template_path.exists():
        print(f"Template not found: {template_path}", file=sys.stderr)
        sys.exit(1)
    if not macros_json_path.exists():
        print(f"Macros JSON not found: {macros_json_path}", file=sys.stderr)
        sys.exit(1)

    # Read and compact the macros JSON
    macros = json.loads(macros_json_path.read_text())
    compact = json.dumps(macros, separators=(",", ":"))

    # Replace placeholder in template
    template = template_path.read_text()
    if "MATHJAX_MACROS_JSON" not in template:
        print(
            "ERROR: MATHJAX_MACROS_JSON placeholder not found in template",
            file=sys.stderr,
        )
        sys.exit(1)

    injected = template.replace("MATHJAX_MACROS_JSON", compact)
    template_path.write_text(injected)
    print(f"Injected {len(macros)} macros into {template_path}")


if __name__ == "__main__":
    main()
