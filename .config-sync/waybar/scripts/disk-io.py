#!/usr/bin/env python3
"""Continuous Waybar disk-I/O meter for the block device backing /."""

from __future__ import annotations

import json
import math
import subprocess
import time
from pathlib import Path

SAMPLE_SECONDS = 1.0
NORMAL_EMIT_SECONDS = 4.0
FAST_EMIT_MIN_GAP_SECONDS = 1.0
SECTOR_BYTES = 512  # Linux block statistics report sectors in 512-byte units.

# Derivative-adaptive low-pass parameters. The displayed quantity is already the
# first derivative of cumulative block counters (MiB/s), so adapting to d(rate)/dt
# makes the filter react to the second derivative of cumulative I/O. Quiet signals
# stay smooth; sharp changes raise the cutoff and propagate quickly.
MIN_CUTOFF_HZ = 0.18
DERIVATIVE_CUTOFF_HZ = 1.0
RATE_BETA = 0.065
BUSY_BETA = 0.025

# The bar normally repaints slowly. A large acceleration or utilization-class
# transition is allowed to interrupt that cadence so bursts appear promptly.
FAST_RATE_DERIVATIVE_MIB_S2 = 12.0
FAST_BUSY_DERIVATIVE_PCT_S = 18.0


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


def lowpass_alpha(cutoff_hz: float, elapsed: float) -> float:
    """Low-pass coefficient for a physical cutoff frequency and sample gap."""
    tau = 1.0 / (2.0 * math.pi * cutoff_hz)
    return 1.0 / (1.0 + tau / elapsed)


class OneEuro:
    """Derivative-adaptive low-pass filter with low lag on sharp transitions."""

    def __init__(self, beta: float):
        self.beta = beta
        self.value: float | None = None
        self.raw: float | None = None
        self.derivative = 0.0

    def update(self, sample: float, elapsed: float) -> tuple[float, float]:
        if self.value is None or self.raw is None:
            self.value = sample
            self.raw = sample
            return sample, 0.0

        raw_derivative = (sample - self.raw) / elapsed
        derivative_alpha = lowpass_alpha(DERIVATIVE_CUTOFF_HZ, elapsed)
        self.derivative += derivative_alpha * (raw_derivative - self.derivative)

        cutoff = MIN_CUTOFF_HZ + self.beta * abs(self.derivative)
        value_alpha = lowpass_alpha(cutoff, elapsed)
        self.value += value_alpha * (sample - self.value)
        self.raw = sample
        return self.value, self.derivative


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
        "Smoothing: derivative-adaptive\n\n"
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

    # Throughput is filtered in MiB/s so RATE_BETA has stable units. IOPS is
    # filtered in kIOPS for the same reason.
    read_rate_filter = OneEuro(RATE_BETA)
    write_rate_filter = OneEuro(RATE_BETA)
    read_iops_filter = OneEuro(RATE_BETA)
    write_iops_filter = OneEuro(RATE_BETA)
    busy_filter = OneEuro(BUSY_BETA)
    css_class = "idle"

    while True:
        time.sleep(SAMPLE_SECONDS)
        now = time.monotonic()
        current = stats(device)
        elapsed = now - previous_time
        if elapsed <= 0:
            previous, previous_time = current, now
            continue

        raw_read_bps = max(0, current[1] - previous[1]) * SECTOR_BYTES / elapsed
        raw_write_bps = max(0, current[3] - previous[3]) * SECTOR_BYTES / elapsed
        raw_read_iops = max(0, current[0] - previous[0]) / elapsed
        raw_write_iops = max(0, current[2] - previous[2]) / elapsed
        raw_busy = min(100.0, max(0, current[4] - previous[4]) / (elapsed * 10.0))

        read_mib_s, read_derivative = read_rate_filter.update(raw_read_bps / 1024**2, elapsed)
        write_mib_s, write_derivative = write_rate_filter.update(raw_write_bps / 1024**2, elapsed)
        read_kiops, _ = read_iops_filter.update(raw_read_iops / 1000.0, elapsed)
        write_kiops, _ = write_iops_filter.update(raw_write_iops / 1000.0, elapsed)
        busy_percent, busy_derivative = busy_filter.update(raw_busy, elapsed)

        previous, previous_time = current, now
        next_class = severity(busy_percent, css_class)
        large_derivative = (
            abs(read_derivative) >= FAST_RATE_DERIVATIVE_MIB_S2
            or abs(write_derivative) >= FAST_RATE_DERIVATIVE_MIB_S2
            or abs(busy_derivative) >= FAST_BUSY_DERIVATIVE_PCT_S
        )
        class_changed = next_class != css_class
        since_emit = now - last_emit
        fast_emit = (large_derivative or class_changed) and since_emit >= FAST_EMIT_MIN_GAP_SECONDS
        if not fast_emit and since_emit < NORMAL_EMIT_SECONDS:
            continue

        css_class = next_class
        emit(payload(
            device,
            read_mib_s * 1024**2,
            write_mib_s * 1024**2,
            read_kiops * 1000.0,
            write_kiops * 1000.0,
            busy_percent,
            css_class,
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
