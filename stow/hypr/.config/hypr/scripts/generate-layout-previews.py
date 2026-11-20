#!/usr/bin/env python3
"""Generate TikZ previews for the Hyprland layout picker.

Each preview is a standalone TikZ picture of rounded rectangles, compiled to
SVG and rasterised to PNG for rofi. No raster image library is involved.
"""

from __future__ import annotations

import argparse
import math
import os
import subprocess
import sys
import tempfile
from collections.abc import Callable
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from typing import NamedTuple

W_CM = 8.0
H_CM = 4.5
GAP_CM = 0.08
CORNER_PT = 1.5
PREVIEW_WIDTH = 400
FILL = "89B4FA"
MASTER_RATIO = 0.55
CENTER_RATIO = 0.5
MONOCLE_STEP_CM = 0.22
MONOCLE_MARGIN = 0.02
MONOCLE_SHADES = (0.19, 0.37, 0.55)


class Card(NamedTuple):
    """One window in a preview, in a 0..1 box, top-left origin."""

    x: float
    y: float
    w: float
    h: float
    color: str = "win"


class Layout(NamedTuple):
    """One picker entry and the Hyprland layout it applies.

    `hypr` is the layout name passed to the workspace rule; `orientation` is
    the `layout_opts.orientation` value, empty when the layout takes none.
    `minimum` is the smallest window count at which the layout differs.
    """

    key: str
    label: str
    geometry: Callable[[int], list[Card]]
    hypr: str
    orientation: str = ""
    minimum: int = 1


def blend(color: str, toward: str, t: float) -> str:
    """Mix `color` toward `toward` by `t`."""
    a = [int(color[i : i + 2], 16) for i in (0, 2, 4)]
    b = [int(toward[i : i + 2], 16) for i in (0, 2, 4)]
    return "".join(f"{round(x + (y - x) * t):02X}" for x, y in zip(a, b))


def split(card: Card, side: str, ratio: float = 0.5) -> tuple[Card, Card]:
    if side == "v":
        return (
            Card(card.x, card.y, card.w * ratio, card.h),
            Card(card.x + card.w * ratio, card.y, card.w * (1 - ratio), card.h),
        )
    return (
        Card(card.x, card.y, card.w, card.h * ratio),
        Card(card.x, card.y + card.h * ratio, card.w, card.h * (1 - ratio)),
    )


def dwindle(n: int) -> list[Card]:
    cards = [Card(0.0, 0.0, 1.0, 1.0)]
    for i in range(1, n):
        side = "v" if (i - 1) % 2 == 0 else "h"
        first, second = split(cards[-1], side)
        cards[-1] = first
        cards.append(second)
    return cards


def grid(n: int) -> list[Card]:
    cols = math.ceil(math.sqrt(n))
    rows = math.ceil(n / cols)
    cards = []
    for i in range(n):
        row = i // cols
        col = i % cols
        in_row = min(cols, n - row * cols)
        w = 1.0 / in_row
        h = 1.0 / rows
        cards.append(Card(col * w, row * h, w, h))
    return cards


def columns(n: int) -> list[Card]:
    return [Card(i / n, 0.0, 1.0 / n, 1.0) for i in range(n)]


def rows(n: int) -> list[Card]:
    return [Card(0.0, i / n, 1.0, 1.0 / n) for i in range(n)]


def two_sided(n: int, master_w: float) -> list[Card]:
    """Master column in the middle, stack windows split between both sides."""
    side_w = (1.0 - master_w) / 2
    left_n = (n - 1) // 2
    right_n = n - 1 - left_n
    cards = [Card(side_w, 0.0, master_w, 1.0)]
    for i in range(left_n):
        cards.append(Card(0.0, i / left_n, side_w, 1.0 / left_n))
    for i in range(right_n):
        cards.append(Card(side_w + master_w, i / right_n, side_w, 1.0 / right_n))
    return cards


def center(n: int) -> list[Card]:
    if n == 1:
        return [Card(0.0, 0.0, 1.0, 1.0)]
    if n == 2:
        return [Card(0.0, 0.0, 0.5, 1.0), Card(0.5, 0.0, 0.5, 1.0)]
    return two_sided(n, CENTER_RATIO)


def master_left(n: int) -> list[Card]:
    cards = [Card(0.0, 0.0, MASTER_RATIO, 1.0)]
    for i in range(n - 1):
        cards.append(Card(MASTER_RATIO, i / (n - 1), 1.0 - MASTER_RATIO, 1.0 / (n - 1)))
    return cards


def master_right(n: int) -> list[Card]:
    return [Card(1.0 - c.x - c.w, c.y, c.w, c.h) for c in master_left(n)]


def master_top(n: int) -> list[Card]:
    cards = [Card(0.0, 0.0, 1.0, MASTER_RATIO)]
    for i in range(n - 1):
        cards.append(Card(i / (n - 1), MASTER_RATIO, 1.0 / (n - 1), 1.0 - MASTER_RATIO))
    return cards


def master_bottom(n: int) -> list[Card]:
    return [Card(c.x, 1.0 - c.y - c.h, c.w, c.h) for c in master_top(n)]


def master_center(n: int) -> list[Card]:
    return two_sided(n, MASTER_RATIO)


def monocle(_n: int) -> list[Card]:
    """A deck of windows: the front card full size, the others peeking out."""
    dx = MONOCLE_STEP_CM / W_CM
    dy = MONOCLE_STEP_CM / H_CM
    w = 1.0 - 2 * MONOCLE_MARGIN - 3 * dx
    h = 1.0 - 2 * MONOCLE_MARGIN - 3 * dy
    return [
        Card(MONOCLE_MARGIN + i * dx, MONOCLE_MARGIN + i * dy, w, h, color)
        for i, color in ((3, "win3"), (2, "win2"), (1, "win1"), (0, "win"))
    ]


# Popup order is by prevalence, most common first: `grid` is the everyday
# layout, and the master orientations are the least used.
LAYOUTS = (
    Layout("grid", "Grid", grid, "lua:grid", minimum=3),
    Layout("dwindle", "Dwindle · tree", dwindle, "dwindle"),
    Layout("monocle", "Monocle · stack", monocle, "monocle"),
    Layout("columns", "Columns", columns, "lua:columns", minimum=2),
    Layout("rows", "Rows", rows, "lua:rows", minimum=2),
    Layout("center", "Center focus", center, "lua:center", minimum=3),
    Layout("master-left", "Master · left", master_left, "master", "left", 2),
    Layout("master-right", "Master · right", master_right, "master", "right", 2),
    Layout("master-top", "Master · top", master_top, "master", "top", 2),
    Layout("master-bottom", "Master · bottom", master_bottom, "master", "bottom", 2),
    Layout("master-center", "Master · center", master_center, "master", "center", 3),
)


def options(n: int) -> list[tuple[Layout, str]]:
    out = []
    for layout in LAYOUTS:
        if n < layout.minimum:
            continue
        label = layout.label
        if layout.key == "grid":
            cols = math.ceil(math.sqrt(n))
            rows = math.ceil(n / cols)
            label = f"Grid · {cols}×{rows}"
        elif layout.key == "columns":
            label = f"Columns · {n}"
        elif layout.key == "rows":
            label = f"Rows · {n}"
        out.append((layout, label))
    return out


def tex_for(cards: list[Card]) -> str:
    shades = {"win": FILL}
    for i, t in enumerate(MONOCLE_SHADES, start=1):
        shades[f"win{i}"] = blend(FILL, "000000", t)
    lines = [
        r"\documentclass[tikz,border=0pt]{standalone}",
        r"\usepackage{tikz}",
        *(
            rf"\definecolor{{{name}}}{{HTML}}{{{value}}}"
            for name, value in shades.items()
        ),
        r"\begin{document}",
        r"\begin{tikzpicture}[x=1cm,y=1cm]",
    ]

    for card in cards:
        x0 = card.x * W_CM + GAP_CM
        y0 = (1.0 - card.y - card.h) * H_CM + GAP_CM
        x1 = (card.x + card.w) * W_CM - GAP_CM
        y1 = (1.0 - card.y) * H_CM - GAP_CM
        if x1 <= x0 or y1 <= y0:
            continue
        lines.append(
            rf"\fill[{card.color}, rounded corners={CORNER_PT}pt] "
            rf"({x0:.3f},{y0:.3f}) rectangle ({x1:.3f},{y1:.3f});"
        )

    lines += [r"\end{tikzpicture}", r"\end{document}", ""]
    return "\n".join(lines)


def build(layout: Layout, n: int, out_dir: Path, force: bool = False) -> Path:
    svg = out_dir / f"{layout.key}-{n}.svg"
    png = out_dir / f"{layout.key}-{n}.png"
    if (
        png.exists()
        and not force
        and png.stat().st_mtime >= Path(__file__).resolve().stat().st_mtime
    ):
        return png

    with tempfile.TemporaryDirectory(prefix="layout-preview-") as tmp:
        tmp_path = Path(tmp)
        (tmp_path / "preview.tex").write_text(tex_for(layout.geometry(n)))
        subprocess.run(
            ["pdflatex", "-interaction=batchmode", "-halt-on-error", "preview.tex"],
            cwd=tmp_path,
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        subprocess.run(
            ["pdf2svg", str(tmp_path / "preview.pdf"), str(svg)],
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        subprocess.run(
            ["rsvg-convert", "-w", str(PREVIEW_WIDTH), "-o", str(png), str(svg)],
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
    return png


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Build and list Hyprland layout previews.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument("--count", type=int, help="window count to build for")
    parser.add_argument(
        "--all", action="store_true", help="build every count from 1 to 10"
    )
    parser.add_argument(
        "--list",
        action="store_true",
        help="print the picker entries instead of building",
    )
    parser.add_argument(
        "--force", action="store_true", help="rebuild previews that are up to date"
    )
    parser.add_argument(
        "--out",
        type=Path,
        default=Path.home() / ".cache/hypr/layout-previews",
        help="preview cache directory",
    )
    args = parser.parse_args()

    if args.list:
        if not args.count:
            parser.error("--list requires --count")
        for layout, label in options(args.count):
            print(f"{layout.key}|{label}|{layout.hypr}|{layout.orientation}")
        return 0

    counts = [args.count] if args.count else list(range(1, 11)) if args.all else []
    if not counts:
        parser.error("pass --count N or --all")

    args.out.mkdir(parents=True, exist_ok=True)
    jobs = [(layout, n) for n in counts for layout, _ in options(n)]

    with ThreadPoolExecutor(max_workers=min(8, os.cpu_count() or 1)) as pool:
        futures = {
            pool.submit(build, layout, n, args.out, args.force): (layout, n)
            for layout, n in jobs
        }
        for future in as_completed(futures):
            layout, n = futures[future]
            try:
                future.result()
            except (subprocess.CalledProcessError, OSError) as exc:
                print(f"failed {layout.key}-{n}: {exc}", file=sys.stderr)
                return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
