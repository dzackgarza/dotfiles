#!/usr/bin/env python3
"""
Generate MathJax 3 macro configuration (JS/TS) from canonical LaTeX tier files.

Reads tier1-mathjax-simple.tex and tier2-mathjax-args.tex, parses
\\newcommand / \\def / \\DeclareMathOperator / \\DeclarePairedDelimiter
definitions, and outputs:

  - A JavaScript ESM module exporting a { macros } object
  - A TypeScript module exporting the same with type annotations
  - A JSON file for direct embedding in HTML

MathJax 3 tex.macros format:
  - Zero-arg macros:  "MacroName": "replacement"
  - N-arg macros:     "MacroName": ["replacement with #1..#n", N]
"""

import argparse
import json
import re
import sys
from pathlib import Path
from typing import NamedTuple

REPO_ROOT = Path(__file__).resolve().parent.parent
TIER1 = REPO_ROOT / "styles" / "macros" / "tier1-mathjax-simple.tex"
TIER2 = REPO_ROOT / "styles" / "macros" / "tier2-mathjax-args.tex"
OUT_DIR = REPO_ROOT / "templates" / "css"


class MacroDef(NamedTuple):
    name: str
    arg_count: int
    body: str


# Pattern to locate the start of any macro definition command
DEF_CMD_RE = re.compile(
    r"""
    \\
    (?:newcommand|renewcommand|providecommand
      |DeclareMathOperator|DeclarePairedDelimiter
      |def
    )\*?
    """,
    re.VERBOSE | re.DOTALL,
)

# Lines that are pure comments or empty
_COMMENT_OR_EMPTY = re.compile(r"^\s*(%.*|\s*)$")

# Lines to exclude entirely (preamble boilerplate)
_EXCLUDE_STARTSWITH = (
    "\\NeedsTeXFormat",
    "\\ProvidesPackage",
    "\\usepackage",
    "\\makeatletter",
    "\\makeatother",
    "\\endinput",
)

# Lines to exclude entirely (not macros, or problematic for MathJax)
EXCLUDE_LINES_STARTSWITH = (
    "\\NeedsTeXFormat",
    "\\ProvidesPackage",
    "\\usepackage",
    "\\makeatletter",
    "\\makeatother",
    "\\endinput",
    "\\input{",
)

# Lines that are pure comments or empty
COMMENT_OR_EMPTY = re.compile(r"^\s*(%.*|\s*)$")

# \DeclareMathOperator{{\mathbb{L} }} -> this produces an arg-count issue;
# DeclareMathOperator always wraps in \operatorname{}
DECLARE_MATH_OP_RE = re.compile(
    r"\\DeclareMathOperator\*?\s*\{\s*\\([a-zA-Z@]+)\s*\}\s*\{(.*)\}",
    re.DOTALL,
)


def _strip_comments_and_boilerplate(content: str) -> str:
    """Remove comment-only lines and preamble boilerplate."""
    lines: list[str] = []
    for line in content.splitlines():
        stripped = line.strip()
        if _COMMENT_OR_EMPTY.match(stripped):
            continue
        if stripped.startswith(_EXCLUDE_STARTSWITH):
            continue
        lines.append(line)
    return "\n".join(lines)


def _merge_continuations(raw: str) -> str:
    """Merge lines that end with a trailing % (continuation marker)."""
    lines = raw.splitlines()
    merged: list[str] = []
    i = 0
    while i < len(lines):
        line = lines[i]
        if line.rstrip().endswith("%") and i + 1 < len(lines):
            line = line.rstrip()[:-1]  # strip trailing %
            i += 1
            line += " " + lines[i].lstrip()
        merged.append(line)
        i += 1
    return "\n".join(merged)


def _skip_ws(raw: str, pos: int) -> int:
    """Skip whitespace, return new position."""
    while pos < len(raw) and raw[pos] in " \t\n\r":
        pos += 1
    return pos


def _extract_balanced_group(raw: str, pos: int) -> tuple[str, int]:
    """Extract balanced-brace group starting at raw[pos].  raw[pos] must be '{'.
    Returns (inner_content, position_after_closing_brace).
    """
    assert pos < len(raw) and raw[pos] == "{", (
        f"expected '{{' at pos {pos}, got {raw[pos : pos + 10]!r}"
    )
    depth = 0
    start = pos
    while pos < len(raw):
        ch = raw[pos]
        if ch == "{":
            depth += 1
        elif ch == "}":
            depth -= 1
            if depth == 0:
                return raw[start + 1 : pos], pos + 1
        elif ch == "\\":
            pos += 1  # skip next char (escaped brace)
        pos += 1
    return raw[start + 1 : pos], pos


def _extract_name(raw: str, pos: int) -> tuple[str, int]:
    """Extract macro name from raw[pos:].  Returns (name, new_position)."""
    pos = _skip_ws(raw, pos)
    if pos >= len(raw):
        return "", pos
    if raw[pos] == "{" and pos + 1 < len(raw) and raw[pos + 1] == "\\":
        # {\name} form
        inner, after = _extract_balanced_group(raw, pos)
        assert inner.startswith("\\"), f"expected \\ name in braces, got {inner!r}"
        return inner[1:], after
    if raw[pos] == "\\":
        # \name form
        end = pos + 1
        while end < len(raw) and raw[end].isalpha():
            end += 1
        return raw[pos + 1 : end], end
    return "", pos


def _extract_opt_arg_count(raw: str, pos: int) -> tuple[int, int]:
    """Extract optional [N] arg count. Returns (N, new_position)."""
    pos = _skip_ws(raw, pos)
    if pos < len(raw) and raw[pos] == "[":
        close = raw.find("]", pos)
        if close != -1:
            try:
                n = int(raw[pos + 1 : close])
                return n, close + 1
            except ValueError:
                pass
    return 0, pos


def _extract_body(raw: str, pos: int) -> tuple[str, int]:
    """Extract body from raw[pos:]. raw[pos] must start with '{'.
    Returns (body_text, position_after_closing_brace)."""
    pos = _skip_ws(raw, pos)
    if pos >= len(raw) or raw[pos] != "{":
        return "", pos
    return _extract_balanced_group(raw, pos)


def parse_macros(content: str) -> list[MacroDef]:
    """Parse all \\newcommand, \\def, \\DeclareMathOperator definitions."""
    text = _strip_comments_and_boilerplate(content)
    text = _merge_continuations(text)

    macros: list[MacroDef] = []
    pos = 0

    while True:
        m = DEF_CMD_RE.search(text, pos)
        if not m:
            break

        cmd = m.group(0).lstrip("\\").rstrip("*")
        pos = m.end()
        pos = _skip_ws(text, pos)

        # --- DeclarePairedDelimiter: skip it (not directly usable in MathJax) ---
        if "DeclarePairedDelimiter" in cmd:
            # Consume name, left, right groups and skip
            name, pos = _extract_name(text, pos)
            _body, pos = _extract_body(text, pos)
            _body, pos = _extract_body(text, pos)
            continue

        # --- Extract macro name ---
        name, pos = _extract_name(text, pos)
        if not name:
            continue

        # --- Extract optional arg count ---
        arg_count, pos = _extract_opt_arg_count(text, pos)

        # --- Extract body ---
        body, pos = _extract_body(text, pos)
        body = body.strip()

        if not body:
            continue

        # --- Special handling ---
        if "DeclareMathOperator" in cmd:
            body = f"\\operatorname{{{body}}}"
            arg_count = 0

        macros.append(MacroDef(name=name, arg_count=arg_count, body=body))

    return macros


ESM_HEADER = """\
/**
 * MathJax 3 macro configuration — generated by bin/generate-mathjax-config.py.
 *
 * DO NOT EDIT MANUALLY.  Source of truth:
 *   styles/macros/tier1-mathjax-simple.tex
 *   styles/macros/tier2-mathjax-args.tex
 *
 * Usage (ESM):
 *   import { macros } from "./mathjax-macros.mjs";
 *   MathJax = { tex: { macros } };
 *
 * Usage (MathJax HTML config):
 *   <script>
 *     window.MathJax = {
 *       tex: { macros: { ... } }
 *     };
 *   </script>
 */

"""

TS_HEADER = """\
/**
 * MathJax 3 macro configuration — generated by bin/generate-mathjax-config.py.
 *
 * DO NOT EDIT MANUALLY.  Source of truth:
 *   styles/macros/tier1-mathjax-simple.tex
 *   styles/macros/tier2-mathjax-args.tex
 *
 * Usage:
 *   import { macros } from "./mathjax-macros";
 *   MathJax = { tex: { macros } };
 */

/** A zero-argument macro replacement. */
type ZeroArgMacro = string;

/** A macro with N arguments. */
type NArgMacro = [replacement: string, argCount: number];

/** MathJax 3 tex.macros configuration. */
export const macros: Record<string, ZeroArgMacro | NArgMacro> = {
"""


def _read_file(path: Path) -> str:
    if not path.exists():
        print(f"ERROR: source file not found: {path}", file=sys.stderr)
        sys.exit(1)
    return path.read_text()


def _escape_for_js(body: str) -> str:
    """Make a LaTeX body safe to embed in a JavaScript string literal.

    - Double all backslashes
    - Escape newlines and other control characters via \\n, \\t, etc.
    - Other chars that break JS string literals get \\uXXXX encoding
    """
    body = body.replace("\\", "\\\\")
    # Escape literal newlines (from multiline \\def bodies)
    body = body.replace("\n", "\\n")
    body = body.replace("\r", "\\r")
    body = body.replace("\t", "\\t")
    return body


def _format_0arg(body: str) -> str:
    """Format a zero-arg macro as a JS string."""
    return f'"{_escape_for_js(body)}"'


def _format_narg(body: str, n: int) -> str:
    """Format an N-arg macro as a JS tuple [body, n]."""
    return f'["{_escape_for_js(body)}", {n}]'


def generate_js(macros: list[MacroDef]) -> str:
    """Generate JavaScript ESM module content."""
    lines: list[str] = [ESM_HEADER, "export const macros = {"]

    for m in macros:
        if m.arg_count == 0:
            lines.append(f'  "{m.name}": {_format_0arg(m.body)},')
        else:
            lines.append(f'  "{m.name}": {_format_narg(m.body, m.arg_count)},')

    lines.append("};")
    lines.append("")  # trailing newline
    return "\n".join(lines)


def generate_ts(macros: list[MacroDef]) -> str:
    """Generate TypeScript module content."""
    lines: list[str] = [TS_HEADER]

    for m in macros:
        if m.arg_count == 0:
            lines.append(f'  "{m.name}": {_format_0arg(m.body)},')
        else:
            lines.append(f'  "{m.name}": {_format_narg(m.body, m.arg_count)},')

    lines.append("};\n")
    return "\n".join(lines)


def generate_json(macros: list[MacroDef]) -> str:
    """Generate JSON for embedding in HTML.
    json.dumps handles backslash escaping, so we pass raw LaTeX bodies.
    """
    obj: dict[str, str | list] = {}
    for m in macros:
        if m.arg_count == 0:
            obj[m.name] = m.body
        else:
            obj[m.name] = [m.body, m.arg_count]
    return json.dumps(obj, indent=2)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Generate MathJax 3 macro config from canonical LaTeX tier files."
    )
    parser.add_argument(
        "--tier1",
        type=Path,
        default=TIER1,
        help="Path to tier1-mathjax-simple.tex",
    )
    parser.add_argument(
        "--tier2",
        type=Path,
        default=TIER2,
        help="Path to tier2-mathjax-args.tex",
    )
    parser.add_argument(
        "--out-dir",
        type=Path,
        default=OUT_DIR,
        help="Output directory for generated files.",
    )
    parser.add_argument(
        "--js",
        type=Path,
        default=None,
        help="Output path for .mjs file (default: --out-dir/mathjax-macros.mjs)",
    )
    parser.add_argument(
        "--ts",
        type=Path,
        default=None,
        help="Output path for .ts file (default: --out-dir/mathjax-macros.ts)",
    )
    parser.add_argument(
        "--json",
        type=Path,
        default=None,
        help="Output path for .json file (default: --out-dir/mathjax-macros.json)",
    )
    parser.add_argument(
        "--count",
        action="store_true",
        help="Print macro count summary and exit.",
    )
    args = parser.parse_args()

    tier1_content = _read_file(args.tier1)
    tier2_content = _read_file(args.tier2)

    macros1 = parse_macros(tier1_content)
    macros2 = parse_macros(tier2_content)

    all_macros = macros1 + macros2

    if args.count:
        zero = sum(1 for m in all_macros if m.arg_count == 0)
        narg = sum(1 for m in all_macros if m.arg_count > 0)
        print(
            f"Macros parsed: {len(all_macros)} total ({zero} zero-arg, {narg} with args)"
        )
        return

    out_dir = args.out_dir
    out_dir.mkdir(parents=True, exist_ok=True)

    js_path = args.js or (out_dir / "mathjax-macros.mjs")
    ts_path = args.ts or (out_dir / "mathjax-macros.ts")
    json_path = args.json or (out_dir / "mathjax-macros.json")

    js_content = generate_js(all_macros)
    ts_content = generate_ts(all_macros)
    json_content = generate_json(all_macros)

    js_path.write_text(js_content)
    ts_path.write_text(ts_content)
    json_path.write_text(json_content)

    zero = sum(1 for m in all_macros if m.arg_count == 0)
    narg = sum(1 for m in all_macros if m.arg_count > 0)
    print(
        f"Generated: {js_path} ({len(all_macros)} macros: {zero} zero-arg, {narg} with args)"
    )
    print(f"Generated: {ts_path}")
    print(f"Generated: {json_path}")


if __name__ == "__main__":
    main()
