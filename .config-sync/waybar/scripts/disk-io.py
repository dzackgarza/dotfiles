#!/usr/bin/env python3
"""Continuous Waybar disk-I/O meter for the block device backing /."""

from __future__ import annotations

import json
import os
import subprocess
import time
from pathlib import Path

POLL_SECONDS = 1.0
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
    value = max(0.0, bytes_per_second)
    units = ((1024**3, "G"), (1024**2, "M"), (1024, "K"))
    for scale, suffix in units:
        if value >= scale:
            scaled = value / scale
            return f"{scaled:.0f}{suffix}" if scaled >= 100 else f"{scaled:.1f}{suffix}"
    return f"{value:.0f}B"


def detail_rate(bytes_per_second: float) -> str:
    value = max(0.0, bytes_per_second)
    if value >= 1024**3:
        return f"{value / 1024**3:.2f} GiB/s"
    if value >= 1024**2:
        return f"{value / 1024**2:.2f} MiB/s"
    if value >= 1024:
        return f"{value / 1024:.1f} KiB/s"
    return f"{value:.0f} B/s"


def severity(busy_percent: float) -> str:
    if busy_percent >= 85:
        return "critical"
    if busy_percent >= 60:
        return "warning"
    if busy_percent >= 10:
        return "active"
    return "idle"


def payload(
    device: str,
    read_bps: float,
    write_bps: float,
    read_iops: float,
    write_iops: float,
    busy_percent: float,
) -> dict[str, str]:
    tooltip = (
        f"Disk I/O — {device}\n"
        f"Read:  {detail_rate(read_bps)}  ({read_iops:.0f} IOPS)\n"
        f"Write: {detail_rate(write_bps)}  ({write_iops:.0f} IOPS)\n"
        f"Busy:  {busy_percent:.0f}%\n\n"
        "Left click: device stats (iostat)\n"
        "Right click: per-process I/O (pidstat)"
    )
    return {
        "text": f"R{rate_text(read_bps)} W{rate_text(write_bps)}",
        "tooltip": tooltip,
        "class": severity(busy_percent),
    }


def emit(data: dict[str, str]) -> None:
    print(json.dumps(data), flush=True)


def main() -> None:
    device = root_block_device()
    previous = stats(device)
    previous_time = time.monotonic()

    while True:
        time.sleep(POLL_SECONDS)
        current_time = time.monotonic()
        current = stats(device)
        elapsed = current_time - previous_time
        if elapsed <= 0:
            previous, previous_time = current, current_time
            continue

        read_ios = max(0, current[0] - previous[0]) / elapsed
        read_bps = max(0, current[1] - previous[1]) * SECTOR_BYTES / elapsed
        write_ios = max(0, current[2] - previous[2]) / elapsed
        write_bps = max(0, current[3] - previous[3]) * SECTOR_BYTES / elapsed
        busy_percent = min(100.0, max(0, current[4] - previous[4]) / (elapsed * 10.0))

        emit(payload(device, read_bps, write_bps, read_ios, write_ios, busy_percent))
        previous, previous_time = current, current_time


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        emit({"text": "R? W?", "tooltip": str(exc), "class": "critical"})
        raise
