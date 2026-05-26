#!/usr/bin/env python3
"""Semantic test for tikzcd.lua pandoc filter.

Reads markdown fixtures from tests/fixtures/, runs them through the filter,
and asserts on the re-parsed JSON AST from pandoc's own format readers.
"""

import json
import os
import subprocess
import sys
from pathlib import Path

from bs4 import BeautifulSoup

HERE = Path(__file__).resolve().parent
FILTER = HERE.parent / "filters" / "tikzcd.lua"
FIXTURES = HERE / "fixtures"

passed = 0
failed = 0


def pandoc_transform(input_path: Path, to_fmt: str) -> subprocess.CompletedProcess:
    """Run the filter: transform markdown into to_fmt."""
    return subprocess.run(
        [
            "pandoc",
            "--lua-filter",
            str(FILTER),
            "-f",
            "markdown+raw_tex",
            "-t",
            to_fmt,
            str(input_path),
        ],
        capture_output=True,
        text=True,
    )


def reparse_as_json(text: str, from_fmt: str) -> dict | None:
    """Parse text with pandoc's from_fmt reader, return JSON AST or None."""
    cp = subprocess.run(
        ["pandoc", "-f", from_fmt, "-t", "json"],
        input=text,
        capture_output=True,
        text=True,
    )
    return json.loads(cp.stdout) if cp.returncode == 0 else None


def check(name: str) -> None:
    global passed, failed
    passed += 1
    print(f"  [PASS] {name}")


def fail(name: str, detail: str) -> None:
    global passed, failed
    failed += 1
    print(f"  [FAIL] {name}: {detail}")


# ---------------------------------------------------------------
# AST walk helpers
# ---------------------------------------------------------------


def find_blocks(doc: dict) -> list:
    """Return all blocks from a JSON AST document."""
    return doc.get("blocks", [])


def figure_has_image_with_width(
    figure_block: dict, width_val: str = r"\columnwidth"
) -> bool:
    """Check a Figure block contains an Image with a given width attribute."""
    caption, labels, contents = figure_block["c"]
    for inner in contents:
        inlines = inner.get("c", []) if inner["t"] in ("Plain", "Para") else []
        for il in inlines:
            if il["t"] == "Image":
                _, _, kvs = il["c"][0]  # [id, classes, [(k,v),...]]
                for k, v in kvs:
                    if k == "width" and width_val in v:
                        return True
    return False


def div_has_span_with_image(div_block: dict, span_class: str) -> bool:
    """Check a Div block contains a Span with given class containing an Image."""
    attrs, contents = div_block["c"]
    for inner in contents:
        inlines = inner.get("c", []) if inner["t"] in ("Plain", "Para") else []
        for il in inlines:
            if il["t"] == "Span":
                span_attrs = il["c"][0]  # [id, classes, kvs]
                if span_class in span_attrs[1]:
                    # Check contained inlines for Image
                    for span_inner in il["c"][1]:
                        if isinstance(span_inner, dict) and span_inner["t"] == "Image":
                            return True
    return False


# ---------------------------------------------------------------
# Assertion helpers
# ---------------------------------------------------------------


def assert_latex(name: str, input_path: Path, predicate) -> None:
    """Transform markdown → LaTeX via filter, re-parse LaTeX → JSON AST, assert."""
    cp = pandoc_transform(input_path, "latex")
    if cp.returncode != 0:
        fail(name, f"filter crashed (rc={cp.returncode}): {cp.stderr.strip()}")
        return
    doc = reparse_as_json(cp.stdout, "latex")
    if doc is None:
        fail(name, "re-parsing LaTeX output failed")
        return
    if predicate(doc):
        check(name)
    else:
        fail(name, "AST predicate returned False")


def assert_html(name: str, input_path: Path, predicate) -> None:
    """Transform markdown → HTML via filter, parse DOM with BeautifulSoup, assert."""
    cp = pandoc_transform(input_path, "html")
    if cp.returncode != 0:
        fail(name, f"filter crashed (rc={cp.returncode}): {cp.stderr.strip()}")
        return
    soup = BeautifulSoup(cp.stdout, "html.parser")
    if predicate(soup):
        check(name)
    else:
        fail(name, "DOM predicate returned False")


def assert_exit(name: str, input_path: Path, expected_rc: int = 83) -> None:
    """Assert filter exits with a specific non-zero code (crash test)."""
    cp = pandoc_transform(input_path, "latex")
    if cp.returncode == expected_rc:
        check(name)
    else:
        stderr = cp.stderr.strip() or "(none)"
        fail(name, f"expected rc={expected_rc}, got rc={cp.returncode}: {stderr}")


# ---------------------------------------------------------------
# Tests
# ---------------------------------------------------------------


def test_standalone_template() -> None:
    tpl = HERE.parent / "templates" / "standalone-tikz.tex"
    if tpl.exists():
        check("template file exists")
    else:
        fail("template file exists", f"not found at {tpl}")


def test_svg_directory() -> None:
    d = Path(os.environ.get("FIGURES_DIR", Path.home() / "figures")) / "rendered"
    d.mkdir(parents=True, exist_ok=True)
    if d.is_dir():
        check("SVG directory exists")
    else:
        fail("SVG directory exists", f"cannot create {d}")


# --- tikzcd ---


def test_tikzcd_latex() -> None:
    """LaTeX output: Figure block with Image[width=\\columnwidth]."""
    path = FIXTURES / "tikzcd" / "input.md"

    def check_ast(doc):
        return any(
            b["t"] == "Figure" and figure_has_image_with_width(b)
            for b in find_blocks(doc)
        )

    assert_latex("Figure > Image[width=\\columnwidth]", path, check_ast)


def test_tikzcd_html() -> None:
    """HTML output: Div[text-align:center] > Span.tikzcd > Image."""
    path = FIXTURES / "tikzcd" / "input.md"

    def check_dom(soup):
        div = soup.find("div", style="text-align:center;")
        if not div:
            return False
        span = div.find("span", class_="tikzcd")
        if not span:
            return False
        return span.find("svg") is not None

    assert_html("div.center > span.tikzcd > svg", path, check_dom)


# --- tikzpicture ---


def test_tikzpicture_latex() -> None:
    """LaTeX output: Figure block with Image[width=\\columnwidth]."""
    path = FIXTURES / "tikzpicture" / "input.md"

    def check_ast(doc):
        return any(
            b["t"] == "Figure" and figure_has_image_with_width(b)
            for b in find_blocks(doc)
        )

    assert_latex("Figure > Image[width=\\columnwidth]", path, check_ast)


def test_tikzpicture_html() -> None:
    """HTML output: Div[text-align:center] > Span.tikzpic > svg."""
    path = FIXTURES / "tikzpicture" / "input.md"

    def check_dom(soup):
        div = soup.find("div", style="text-align:center;")
        if not div:
            return False
        span = div.find("span", class_="tikzpic")
        if not span:
            return False
        return span.find("svg") is not None

    assert_html("div.center > span.tikzpic > svg", path, check_dom)


# --- fenced div (filter processes nested RawBlock) ---


def test_fenced_div_latex() -> None:
    """Fenced div with tikzcd: filter processes nested RawBlock, same as top-level."""
    path = FIXTURES / "fenced-div" / "input.md"

    def check_ast(doc):
        return any(
            b["t"] == "Figure" and figure_has_image_with_width(b)
            for b in find_blocks(doc)
        )

    assert_latex("Figure > Image[width=\\columnwidth]", path, check_ast)


def test_fenced_div_html() -> None:
    """Fenced div with tikzcd: produces <svg> (filter processes nested RawBlocks)."""
    path = FIXTURES / "fenced-div" / "input.md"

    def check_dom(soup):
        return soup.find("svg") is not None

    assert_html("contains <svg>", path, check_dom)


# --- multiple blocks ---


def test_multiple_blocks_latex() -> None:
    """Two tikz blocks in one document → 2 Figure blocks."""
    path = FIXTURES / "multiple-blocks" / "input.md"

    def check_ast(doc):
        figures = [
            b
            for b in find_blocks(doc)
            if b["t"] == "Figure" and figure_has_image_with_width(b)
        ]
        return len(figures) == 2

    assert_latex("2 Figure blocks with Image", path, check_ast)


def test_multiple_blocks_html() -> None:
    """Two tikz blocks → 2 <svg> elements."""
    path = FIXTURES / "multiple-blocks" / "input.md"

    def check_dom(soup):
        return len(soup.find_all("svg")) == 2

    assert_html("2 <svg> elements", path, check_dom)


# --- tikz code block (```tikz) ---


def test_tikzcode_latex() -> None:
    """```tikz code block: Figure with Image[width=\\columnwidth]."""
    path = FIXTURES / "tikzcode" / "input.md"

    def check_ast(doc):
        figures = [
            b
            for b in find_blocks(doc)
            if b["t"] == "Figure" and figure_has_image_with_width(b)
        ]
        # Exactly 1 figure (the ```tikz block), not 2 (python block not compiled)
        return len(figures) == 1

    assert_latex("1 Figure block, python block not compiled", path, check_ast)


def test_tikzcode_html() -> None:
    """```tikz code block: Div > Span.tikzcode > svg."""
    path = FIXTURES / "tikzcode" / "input.md"

    def check_dom(soup):
        div = soup.find("div", style="text-align:center;")
        if not div:
            return False
        span = div.find("span", class_="tikzcode")
        if not span:
            return False
        return span.find("svg") is not None

    assert_html("div.center > span.tikzcode > svg", path, check_dom)


# --- crash handling ---


def test_bad_tikz_crashes() -> None:
    """Invalid tikz must crash (pandoc exits 83 for Lua filter error)."""
    path = FIXTURES / "bad-tikz" / "input.md"
    assert_exit("crashes on invalid tikz", path, expected_rc=83)


# ---------------------------------------------------------------
def main() -> None:
    tests = [
        (
            "infrastructure",
            [
                test_standalone_template,
                test_svg_directory,
            ],
        ),
        (
            "tikzcd",
            [
                test_tikzcd_latex,
                test_tikzcd_html,
            ],
        ),
        (
            "tikzpicture",
            [
                test_tikzpicture_latex,
                test_tikzpicture_html,
            ],
        ),
        (
            "fenced div with tikzcd",
            [
                test_fenced_div_latex,
                test_fenced_div_html,
            ],
        ),
        (
            "multiple blocks",
            [
                test_multiple_blocks_latex,
                test_multiple_blocks_html,
            ],
        ),
        (
            "tikz code block (```tikz)",
            [
                test_tikzcode_latex,
                test_tikzcode_html,
            ],
        ),
        (
            "crash handling",
            [
                test_bad_tikz_crashes,
            ],
        ),
    ]

    for group_name, group_tests in tests:
        print(f"\n=== {group_name} ===")
        for t in group_tests:
            t()

    total = passed + failed
    print(f"\n{'=' * 50}")
    print(f"  {passed}/{total} passed, {failed} failed")
    sys.exit(1 if failed > 0 else 0)


if __name__ == "__main__":
    main()
