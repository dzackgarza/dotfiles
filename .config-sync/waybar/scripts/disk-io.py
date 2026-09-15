#!/usr/bin/env python3
"""Continuous Waybar disk-I/O meter for the block device backing /."""

from __future__ import annotations

import json
import math
import subprocess
import time
from pathlib import Path

SAMPLE_SECONDS = 1.0
EMIT_SECONDS = 2.0
EMA_HALF_LIFE_SECONDS = 2.0
SECTOR_BYTES = 512  # Linux block statistics report sectors in 512-byte units.


def root_block_device() -> str:
    source = subprocess.check_output(["findmnt", "-no", "SOURCE", "/"], text=True).strip()
    if not source.startswith("/dev/"):
        raise RuntimeError(f"root filesystem is not backed by a block device: {source}")

    name = Path(source).name
    sys_block = Path("/sys/class/block") / name
    if not sys_block.exists():
        raise RuntimeError(f"block device is missing from sysfs: {name}")

    # Whole-device statistics include all activity on the root partition. For
    # nvme0n1p2, for example, the resolved sysfs parent is nvme0n1.
    if (sys_block / "partition").exists():
        name = sys_block.resolve().parent.name
    return name


def stats(device: str) -> tuple[int, int, int, int, int]:
    fields = (Path("/sys/class/block") / device / "stat").read_text().split()
    if len(fields) < 10:
        raise RuntimeError(f"unexpected /sys/class/block/{device}/stat format")
    return (
        int(fields[0]),  # completed reads
        int(fields[2]),  # sectors read
        int(fields[4]),  # completed writes
        int(fields[6]),  # sectors written
        int(fields[9]),  # milliseconds spent doing I/O
    )


def rate_text(bytes_per_second: float) -> str:
    """Compact bar text: whole MiB/s; precision stays in the tooltip."""
    mib_per_second = max(0.0, bytes_per_second) / 1024**2
    return f"{round(mib_per_second):.0f}M"


def detail_rate(bytes_per_second: float) -> str:
    value = max(0.0, bytes_per_second)
    if value >= 1024**3:
        return f"{value / 1024**3:.2f} GiB/s"
    if value >= 1024**2:
        return f"{value / 1024**2:.2f} MiB/s"
    if value >= 1024:
        return f"{value / 1024:.1f} KiB/s"
    return f"{value:.0f} B/s"


def severity(busy_percent: float, previous: str) -> str:
    """Severity with hysteresis so colour does not flap near thresholds."""
    if previous == "critical":
        if busy_percent >= 72:
            return "critical"
    elif previous == "warning":
        if busy_percent >= 88:
            return "critical"
        if busy_percent >= 48:
            return "warning"
    elif previous == "active":
        if busy_percent >= 88:
            return "critical"
        if busy_percent >= 62:
            return "warning"
        if busy_percent >= 7:
            return "active"
    else:
        if busy_percent >= 88:
            return "critical"
        if busy_percent >= 62:
            return "warning"
        if busy_percent >= 12:
            return "active"

    if busy_percent >= 62:
        return "warning"
    if busy_percent >= 12:
        return "active"
    return "idle"


def ema(previous: float | None, sample: float, elapsed: float) -> float:
    """Time-correct exponential smoothing with a short, explicit half-life."""
    if previous is None:
        return sample
    alpha = 1.0 - math.pow(0.5, elapsed / EMA_HALF_LIFE_SECONDS)
    return previous + alpha * (sample - previous)


def payload(
    device: str,
    read_bps: float,
    write_bps: float,
    read_iops: float,
    write_iops: float,
    busy_percent: float,
    css_class: str,
) -> dict[str, str]:
    tooltip = (
        f"Disk I/O — {device}\n"
        f"Read:  {detail_rate(read_bps)}  ({read_iops:.0f} IOPS)\n"
        f"Write: {detail_rate(write_bps)}  ({write_iops:.0f} IOPS)\n"
        f"Busy:  {busy_percent:.0f}%\n"
        f"Smoothing: {EMA_HALF_LIFE_SECONDS:.0f}s EMA half-life\n\n"
        "Left click: device stats (iostat)\n"
        "Right click: per-process I/O (pidstat)"
    )
    return {
        "text": f"↑{rate_text(read_bps)} ↓{rate_text(write_bps)}",
        "tooltip": tooltip,
        "class": css_class,
    }


def emit(data: dict[str, str]) -> None:
    print(json.dumps(data), flush=True)


def main() -> None:
    device = root_block_device()
    previous = stats(device)
    previous_time = time.monotonic()
    last_emit = previous_time
    smoothed: list[float | None] = [None, None, None, None, None]
    css_class = "idle"

    while True:
        time.sleep(SAMPLE_SECONDS)
        now = time.monotonic()
        current = stats(device)
        elapsed = now - previous_time
        if elapsed <= 0:
            previous, previous_time = current, now
            continue

        samples = (
            max(0, current[1] - previous[1]) * SECTOR_BYTES / elapsed,
            max(0, current[3] - previous[3]) * SECTOR_BYTES / elapsed,
            max(0, current[0] - previous[0]) / elapsed,
            max(0, current[2] - previous[2]) / elapsed,
            min(100.0, max(0, current[4] - previous[4]) / (elapsed * 10.0)),
        )
        for index, sample in enumerate(samples):
            smoothed[index] = ema(smoothed[index], sample, elapsed)

        previous, previous_time = current, now
        if now - last_emit < EMIT_SECONDS:
            continue

        read_bps, write_bps, read_iops, write_iops, busy_percent = (
            float(value) for value in smoothed
        )
        css_class = severity(busy_percent, css_class)
        emit(payload(
            device, read_bps, write_bps, read_iops, write_iops, busy_percent, css_class
        ))
        last_emit = now


if __name__ == "__main__":
    try:
        main()
    except BrokenPipeError:
        pass
    except Exception as exc:
        emit({"text": "↑? ↓?", "tooltip": str(exc), "class": "critical"})
        raise
