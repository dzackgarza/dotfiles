#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.12"
# dependencies = ["cyclopts>=3", "pydantic>=2"]
# ///
"""Generate TikZ previews for the Hyprland layout picker.

Each preview is a standalone TikZ picture of rounded rectangles, compiled to
SVG and rasterised to PNG for rofi. No raster image library is involved.
"""

from __future__ import annotations

import math
import os
import subprocess
import sys
import tempfile
from collections.abc import Callable
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

from cyclopts import App
from pydantic import BaseModel, ConfigDict, Field, TypeAdapter, model_validator

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
ASSETS_DIR = Path(__file__).resolve().parent.parent / "assets/layout-previews"
DEFINITIONS_PATH = Path(__file__).resolve().parent.parent / "confs/layout-picker.json"


class Card(BaseModel):
    """One window in a preview, in a 0..1 box, top-left origin."""

    model_config = ConfigDict(frozen=True, strict=True)

    x: float
    y: float
    w: float
    h: float
    color: str = "win"


class LayoutDefinition(BaseModel):
    """One picker entry and the Hyprland layout it applies."""

    model_config = ConfigDict(frozen=True)

    key: str
    label: str
    hypr: str
    orientation: str = ""
    minimum: int = 1


class Layout(LayoutDefinition):
    """A picker entry paired with its preview geometry."""

    geometry: Callable[[int], list[Card]]


class PreviewOptions(BaseModel):
    """Command line contract."""

    model_config = ConfigDict(frozen=True, strict=True)

    count: int | None = Field(default=None, description="window count to build for")
    all: bool = Field(default=False, description="build every count from 1 to 10")
    force: bool = Field(default=False, description="rebuild up-to-date previews")
    out: Path = Field(
        default=ASSETS_DIR,
        description="preview directory",
    )

    @model_validator(mode="after")
    def _consistent(self) -> PreviewOptions:
        if self.count is None and not self.all:
            raise ValueError("pass --count N or --all")
        return self


def blend(color: str, toward: str, t: float) -> str:
    """Mix `color` toward `toward` by `t`."""
    a = [int(color[i : i + 2], 16) for i in (0, 2, 4)]
    b = [int(toward[i : i + 2], 16) for i in (0, 2, 4)]
    return "".join(f"{round(x + (y - x) * t):02X}" for x, y in zip(a, b))


def split(card: Card, side: str, ratio: float = 0.5) -> tuple[Card, Card]:
    if side == "v":
        return (
            Card(x=card.x, y=card.y, w=card.w * ratio, h=card.h),
            Card(x=card.x + card.w * ratio, y=card.y, w=card.w * (1 - ratio), h=card.h),
        )
    return (
        Card(x=card.x, y=card.y, w=card.w, h=card.h * ratio),
        Card(x=card.x, y=card.y + card.h * ratio, w=card.w, h=card.h * (1 - ratio)),
    )


def dwindle(n: int) -> list[Card]:
    cards = [Card(x=0.0, y=0.0, w=1.0, h=1.0)]
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
        cards.append(Card(x=col * w, y=row * h, w=w, h=h))
    return cards


def columns(n: int) -> list[Card]:
    return [Card(x=i / n, y=0.0, w=1.0 / n, h=1.0) for i in range(n)]


def rows(n: int) -> list[Card]:
    return [Card(x=0.0, y=i / n, w=1.0, h=1.0 / n) for i in range(n)]


def two_sided(n: int, master_w: float) -> list[Card]:
    """Master column in the middle, stack windows split between both sides."""
    side_w = (1.0 - master_w) / 2
    left_n = (n - 1) // 2
    right_n = n - 1 - left_n
    cards = [Card(x=side_w, y=0.0, w=master_w, h=1.0)]
    for i in range(left_n):
        cards.append(Card(x=0.0, y=i / left_n, w=side_w, h=1.0 / left_n))
    for i in range(right_n):
        cards.append(
            Card(x=side_w + master_w, y=i / right_n, w=side_w, h=1.0 / right_n)
        )
    return cards


def center(n: int) -> list[Card]:
    if n == 1:
        return [Card(x=0.0, y=0.0, w=1.0, h=1.0)]
    if n == 2:
        return [
            Card(x=0.0, y=0.0, w=0.5, h=1.0),
            Card(x=0.5, y=0.0, w=0.5, h=1.0),
        ]
    return two_sided(n, CENTER_RATIO)


def master_left(n: int) -> list[Card]:
    cards = [Card(x=0.0, y=0.0, w=MASTER_RATIO, h=1.0)]
    for i in range(n - 1):
        cards.append(
            Card(
                x=MASTER_RATIO,
                y=i / (n - 1),
                w=1.0 - MASTER_RATIO,
                h=1.0 / (n - 1),
            )
        )
    return cards


def master_right(n: int) -> list[Card]:
    return [Card(x=1.0 - c.x - c.w, y=c.y, w=c.w, h=c.h) for c in master_left(n)]


def master_top(n: int) -> list[Card]:
    cards = [Card(x=0.0, y=0.0, w=1.0, h=MASTER_RATIO)]
    for i in range(n - 1):
        cards.append(
            Card(
                x=i / (n - 1),
                y=MASTER_RATIO,
                w=1.0 / (n - 1),
                h=1.0 - MASTER_RATIO,
            )
        )
    return cards


def master_bottom(n: int) -> list[Card]:
    return [Card(x=c.x, y=1.0 - c.y - c.h, w=c.w, h=c.h) for c in master_top(n)]


def master_center(n: int) -> list[Card]:
    return two_sided(n, MASTER_RATIO)


def monocle(_n: int) -> list[Card]:
    """A deck of windows: the front card full size, the others peeking out."""
    dx = MONOCLE_STEP_CM / W_CM
    dy = MONOCLE_STEP_CM / H_CM
    w = 1.0 - 2 * MONOCLE_MARGIN - 3 * dx
    h = 1.0 - 2 * MONOCLE_MARGIN - 3 * dy
    return [
        Card(
            x=MONOCLE_MARGIN + i * dx,
            y=MONOCLE_MARGIN + i * dy,
            w=w,
            h=h,
            color=color,
        )
        for i, color in ((3, "win3"), (2, "win2"), (1, "win1"), (0, "win"))
    ]


GEOMETRY = {
    "grid": grid,
    "dwindle": dwindle,
    "monocle": monocle,
    "columns": columns,
    "rows": rows,
    "center": center,
    "master-left": master_left,
    "master-right": master_right,
    "master-top": master_top,
    "master-bottom": master_bottom,
    "master-center": master_center,
}
DEFINITIONS = TypeAdapter(list[LayoutDefinition]).validate_json(
    DEFINITIONS_PATH.read_bytes()
)
LAYOUTS = tuple(
    Layout(**definition.model_dump(), geometry=GEOMETRY[definition.key])
    for definition in DEFINITIONS
)


def eligible(n: int) -> list[Layout]:
    return [layout for layout in LAYOUTS if n >= layout.minimum]


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
    png = out_dir / f"{layout.key}-{n}.png"
    if png.exists() and not force:
        return png

    with tempfile.TemporaryDirectory(prefix="layout-preview-") as tmp:
        tmp_path = Path(tmp)
        svg = tmp_path / "preview.svg"
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


app = App(name="generate-layout-previews")


@app.default
def main(
    count: int | None = None,
    all: bool = False,
    force: bool = False,
    out: Path = ASSETS_DIR,
) -> int:
    """Build Hyprland layout previews.

    Args:
        count: Window count to build for.
        all: Build every count from 1 to 10.
        force: Rebuild previews that are up to date.
        out: Preview directory.
    """
    opts = PreviewOptions(count=count, all=all, force=force, out=out)

    if opts.all:
        counts = range(1, 11)
    else:
        assert opts.count is not None
        counts = [opts.count]

    opts.out.mkdir(parents=True, exist_ok=True)
    jobs = [(layout, n) for n in counts for layout, _ in options(n)]

    with ThreadPoolExecutor(max_workers=min(8, os.cpu_count() or 1)) as pool:
        futures = {
            pool.submit(build, layout, n, opts.out, opts.force): (layout, n)
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
    app()
