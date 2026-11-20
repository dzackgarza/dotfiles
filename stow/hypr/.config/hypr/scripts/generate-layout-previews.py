#!/usr/bin/env python3
"""Generate TikZ previews for the Hyprland layout picker.

Each preview is a standalone TikZ picture of simple rectangles, compiled to
SVG. No raster image library is involved.
"""

from __future__ import annotations

import argparse
import math
import os
import shutil
import subprocess
import sys
import tempfile
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

W_CM = 8.0
H_CM = 4.5
GAP_CM = 0.08
FILL = "89B4FA"


def split(rect, side, ratio=0.5):
    x, y, w, h = rect
    if side == "v":
        return (x, y, w * ratio, h), (x + w * ratio, y, w * (1 - ratio), h)
    return (x, y, w, h * ratio), (x, y + h * ratio, w, h * (1 - ratio))


def dwindle(n):
    rects = [(0.0, 0.0, 1.0, 1.0)]
    for i in range(1, n):
        side = "v" if (i - 1) % 2 == 0 else "h"
        first, second = split(rects[-1], side)
        rects[-1] = first
        rects.append(second)
    return rects


def grid(n):
    cols = math.ceil(math.sqrt(n))
    rows = math.ceil(n / cols)
    out = []
    for i in range(n):
        row = i // cols
        col = i % cols
        in_row = min(cols, n - row * cols)
        w = 1.0 / in_row
        h = 1.0 / rows
        out.append((col * w, row * h, w, h))
    return out


def columns(n):
    return [(i / n, 0.0, 1.0 / n, 1.0) for i in range(n)]


def rows(n):
    return [(0.0, i / n, 1.0, 1.0 / n) for i in range(n)]


def center(n):
    if n == 1:
        return [(0.0, 0.0, 1.0, 1.0)]
    if n == 2:
        return [(0.0, 0.0, 0.5, 1.0), (0.5, 0.0, 0.5, 1.0)]

    left_n = (n - 1) // 2
    right_n = n - 1 - left_n
    center_w = 0.5
    side_w = (1.0 - center_w) / 2

    out = [(side_w, 0.0, center_w, 1.0)]
    for i in range(left_n):
        out.append((0.0, i / left_n, side_w, 1.0 / left_n))
    for i in range(right_n):
        out.append((side_w + center_w, i / right_n, side_w, 1.0 / right_n))
    return out


def master_left(n):
    master_w = 0.55
    out = [(0.0, 0.0, master_w, 1.0)]
    for i in range(n - 1):
        out.append((master_w, i / (n - 1), 1.0 - master_w, 1.0 / (n - 1)))
    return out


def master_right(n):
    return [(1.0 - x - w, y, w, h) for x, y, w, h in master_left(n)]


def master_top(n):
    master_h = 0.55
    out = [(0.0, 0.0, 1.0, master_h)]
    for i in range(n - 1):
        out.append((i / (n - 1), master_h, 1.0 / (n - 1), 1.0 - master_h))
    return out


def master_bottom(n):
    return [(x, 1.0 - y - h, w, h) for x, y, w, h in master_top(n)]


def monocle(_n):
    return [(0.0, 0.0, 1.0, 1.0)]


LAYOUTS = {
    "dwindle": ("Dwindle · tree", dwindle),
    "master-left": ("Master · left", master_left),
    "master-right": ("Master · right", master_right),
    "master-top": ("Master · top", master_top),
    "master-bottom": ("Master · bottom", master_bottom),
    "master-center": ("Master · center", center),
    "columns": ("Columns", columns),
    "rows": ("Rows", rows),
    "grid": ("Grid", grid),
    "center": ("Center focus", center),
    "monocle": ("Monocle · stack", monocle),
}


def options(n):
    keys = ["dwindle"]
    if n >= 2:
        keys += ["master-left", "master-right", "master-top", "master-bottom", "columns", "rows"]
    if n >= 3:
        keys += ["master-center", "grid", "center"]
    keys.append("monocle")
    return [(key, LAYOUTS[key][0]) for key in keys]


def tex_for(rects):
    lines = [
        r"\documentclass[tikz,border=0pt]{standalone}",
        r"\usepackage{tikz}",
        rf"\definecolor{{win}}{{HTML}}{{{FILL}}}",
        r"\begin{document}",
        r"\begin{tikzpicture}[x=1cm,y=1cm]",
    ]

    for x, y, w, h in rects:
        x0 = x * W_CM + GAP_CM
        y0 = (1.0 - y - h) * H_CM + GAP_CM
        x1 = (x + w) * W_CM - GAP_CM
        y1 = (1.0 - y) * H_CM - GAP_CM
        if x1 <= x0 or y1 <= y0:
            continue
        lines.append(
            rf"\fill[win, rounded corners=1.5pt] "
            rf"({x0:.3f},{y0:.3f}) rectangle ({x1:.3f},{y1:.3f});"
        )

    lines += [r"\end{tikzpicture}", r"\end{document}", ""]
    return "\n".join(lines)


def build(key, n, out_dir, force=False):
    out = out_dir / f"{key}-{n}.svg"
    if out.exists() and not force:
        return out

    with tempfile.TemporaryDirectory(prefix="layout-preview-") as tmp:
        tmp_path = Path(tmp)
        (tmp_path / "preview.tex").write_text(tex_for(LAYOUTS[key][1](n)))
        subprocess.run(
            ["pdflatex", "-interaction=batchmode", "-halt-on-error", "preview.tex"],
            cwd=tmp_path,
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        subprocess.run(
            ["pdf2svg", str(tmp_path / "preview.pdf"), str(out)],
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
    return out


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--count", type=int)
    parser.add_argument("--all", action="store_true")
    parser.add_argument("--list", action="store_true")
    parser.add_argument("--force", action="store_true")
    parser.add_argument("--out", type=Path, default=Path.home() / ".cache/hypr/layout-previews")
    args = parser.parse_args()

    if args.list:
        if not args.count:
            parser.error("--list requires --count")
        for key, label in options(args.count):
            print(f"{key}|{label}")
        return 0

    if not shutil.which("pdflatex") or not shutil.which("pdf2svg"):
        print("pdflatex and pdf2svg are required", file=sys.stderr)
        return 1

    counts = [args.count] if args.count else list(range(1, 11)) if args.all else []
    if not counts:
        parser.error("pass --count N or --all")

    args.out.mkdir(parents=True, exist_ok=True)
    jobs = [(key, n) for n in counts for key, _ in options(n)]

    with ThreadPoolExecutor(max_workers=min(8, os.cpu_count() or 1)) as pool:
        futures = {pool.submit(build, key, n, args.out, args.force): (key, n) for key, n in jobs}
        for future in as_completed(futures):
            key, n = futures[future]
            try:
                future.result()
            except Exception as exc:
                print(f"failed {key}-{n}: {exc}", file=sys.stderr)
                return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
