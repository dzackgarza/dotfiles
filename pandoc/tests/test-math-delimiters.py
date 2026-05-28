#!/usr/bin/env python3
"""Contract tests for convert_math_delimiters.lua.

The filter owns normalization from raw display math delimiters to alignable
equations. These tests exercise Pandoc's real markdown reader and writers.
"""

from pathlib import Path
import subprocess
import sys


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
FILTER = ROOT / "filters" / "convert_math_delimiters.lua"
FIXTURES = HERE / "fixtures" / "math-delimiters"
BUILD_DIR = ROOT / ".build_test_math_delimiters"

passed = 0
failed = 0


def run_pandoc(input_path: Path, to_fmt: str, *extra: str) -> subprocess.CompletedProcess:
    return subprocess.run(
        [
            "pandoc",
            "--lua-filter",
            str(FILTER),
            "-f",
            "markdown+raw_tex+tex_math_single_backslash",
            "-t",
            to_fmt,
            *extra,
            str(input_path),
        ],
        capture_output=True,
        text=True,
    )


def check(name: str) -> None:
    global passed
    passed += 1
    print(f"  [PASS] {name}")


def fail(name: str, detail: str) -> None:
    global failed
    failed += 1
    print(f"  [FAIL] {name}: {detail}")


def assert_output(name: str, cp: subprocess.CompletedProcess, predicate) -> None:
    if cp.returncode != 0:
        fail(name, f"pandoc failed rc={cp.returncode}: {cp.stderr.strip()}")
        return
    if predicate(cp.stdout):
        check(name)
    else:
        fail(name, cp.stdout)


def has_one(text: str, needle: str) -> bool:
    return text.count(needle) == 1


def has_no_display_delimiter_lines(text: str) -> bool:
    lines = {line.strip() for line in text.splitlines()}
    return r"\[" not in lines and r"\]" not in lines and "$$" not in lines


def test_latex_output_aligns_sample() -> None:
    cp = run_pandoc(FIXTURES / "sample.md", "latex")
    assert_output(
        "latex sample uses align*",
        cp,
        lambda out: "\\begin{align*}" in out
        and "\\Set &\\mapstofrom{}{} \\mathrm{CAlg}_k" in out
        and has_no_display_delimiter_lines(out),
    )


def test_markdown_output_aligns_sample() -> None:
    cp = run_pandoc(FIXTURES / "sample.md", "markdown")
    assert_output(
        "markdown sample uses align*",
        cp,
        lambda out: "\\begin{align*}" in out
        and "\\Set &\\mapstofrom{}{} \\mathrm{CAlg}_k" in out
        and has_no_display_delimiter_lines(out),
    )


def test_html_output_aligns_sample() -> None:
    cp = run_pandoc(FIXTURES / "sample.md", "html", "--mathjax")
    assert_output(
        "html sample uses MathJax align*",
        cp,
        lambda out: '<span class="math display">' in out
        and "\\begin{align*}" in out
        and "\\Set &\\mapstofrom{}{} \\mathrm{CAlg}_k" in out
        and has_no_display_delimiter_lines(out),
    )


def test_labeled_display_uses_numbered_align() -> None:
    cp = run_pandoc(FIXTURES / "label.md", "latex")
    assert_output(
        "labelled display uses align",
        cp,
        lambda out: "\\begin{align}" in out
        and "\\begin{equation}" not in out
        and "\\label{eq:energy}" in out,
    )


def test_prewrapped_align_is_not_double_wrapped() -> None:
    for fmt in ("latex", "markdown", "html"):
        cp = run_pandoc(FIXTURES / "already-align.md", fmt)
        assert_output(
            f"{fmt} prewrapped align is single align*",
            cp,
            lambda out: has_one(out, "\\begin{align*}")
            and has_one(out, "\\end{align*}")
            and has_no_display_delimiter_lines(out),
        )


def test_pdf_compiles_sample() -> None:
    BUILD_DIR.mkdir(exist_ok=True)
    out_path = BUILD_DIR / "math-delimiters.pdf"
    cp = subprocess.run(
        [
            "pandoc",
            "--lua-filter",
            str(FILTER),
            "-f",
            "markdown+raw_tex+tex_math_single_backslash",
            "-V",
            "header-includes=" + (FIXTURES / "header.tex").read_text(),
            "--pdf-engine",
            "pdflatex",
            "-o",
            str(out_path),
            str(FIXTURES / "sample.md"),
        ],
        capture_output=True,
        text=True,
        cwd=ROOT,
    )
    if cp.returncode != 0:
        fail("pdf sample compiles", cp.stderr.strip())
        return
    if out_path.exists() and out_path.stat().st_size > 0:
        check("pdf sample compiles")
    else:
        fail("pdf sample compiles", f"missing or empty {out_path}")


def test_pdf_compiles_sample_with_unified_style() -> None:
    BUILD_DIR.mkdir(exist_ok=True)
    out_path = BUILD_DIR / "math-delimiters-unified.pdf"
    cp = subprocess.run(
        [
            "pandoc",
            "--lua-filter",
            str(FILTER),
            "-f",
            "markdown+raw_tex+tex_math_single_backslash",
            "-V",
            r"header-includes=\usepackage{dzg-unified}",
            "--pdf-engine",
            "pdflatex",
            "-o",
            str(out_path),
            str(FIXTURES / "sample.md"),
        ],
        capture_output=True,
        text=True,
        cwd=ROOT,
    )
    if cp.returncode != 0:
        fail("pdf sample compiles with dzg-unified", cp.stderr.strip())
        return
    if out_path.exists() and out_path.stat().st_size > 0:
        check("pdf sample compiles with dzg-unified")
    else:
        fail("pdf sample compiles with dzg-unified", f"missing or empty {out_path}")


def main() -> None:
    tests = [
        test_latex_output_aligns_sample,
        test_markdown_output_aligns_sample,
        test_html_output_aligns_sample,
        test_labeled_display_uses_numbered_align,
        test_prewrapped_align_is_not_double_wrapped,
        test_pdf_compiles_sample,
        test_pdf_compiles_sample_with_unified_style,
    ]
    for test in tests:
        test()
    total = passed + failed
    print(f"\n{'=' * 50}")
    print(f"  {passed}/{total} passed, {failed} failed")
    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    main()
