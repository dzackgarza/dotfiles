#!/usr/bin/env python3
"""Waybar notification indicator backed by swaync-client."""

import json
import subprocess
import sys
from pathlib import Path


SWAYNC_CLIENT = Path("/bin/swaync-client")
BELL = "󰂚"
BELL_OFF = "󰂛"
GREEN, YELLOW, RED = "#aad94c", "#ffb454", "#f07178"
COLOR_STOPS = ((0, GREEN), (50, YELLOW), (100, RED))


def _count(text: str) -> int:
    return int(text) if text.isdecimal() else 0


def _rgb(color: str) -> tuple[int, int, int]:
    return tuple(int(color[index : index + 2], 16) for index in (1, 3, 5))


def _mix(start: str, end: str, ratio: float) -> str:
    channels = [
        int(start_channel + (end_channel - start_channel) * ratio)
        for start_channel, end_channel in zip(_rgb(start), _rgb(end))
    ]
    return "#" + "".join(f"{channel:02x}" for channel in channels)


def _severity(count: int) -> str:
    if count <= COLOR_STOPS[0][0]:
        return GREEN
    if count >= COLOR_STOPS[-1][0]:
        return RED

    lower, upper = (
        (COLOR_STOPS[0], COLOR_STOPS[1])
        if count <= COLOR_STOPS[1][0]
        else (COLOR_STOPS[1], COLOR_STOPS[2])
    )
    lower_count, lower_color = lower
    upper_count, upper_color = upper
    ratio = (count - lower_count) / (upper_count - lower_count)
    return _mix(lower_color, upper_color, ratio)


def render_payload(status: dict) -> dict:
    text = str(status.get("text") or "").strip()
    count_value = _count(text)
    color = _severity(count_value)
    alt = str(status.get("alt") or "")
    css_class = status.get("class") or alt or "none"
    dnd = "dnd" in alt or "dnd" in str(css_class)
    icon = BELL_OFF if dnd else BELL
    count = ""
    if count_value > 0:
        count = f"<span foreground='{color}' size='x-small' rise='4500'>{count_value}</span>"
    return {
        "text": f"<span foreground='{color}'>{icon}</span>{count}",
        "tooltip": status.get("tooltip") or "Notifications",
        "class": css_class,
    }


def main() -> None:
    assert SWAYNC_CLIENT.is_file(), f"swaync-client is required at {SWAYNC_CLIENT}"
    process = subprocess.Popen(
        [SWAYNC_CLIENT, "-swb"],
        stdout=subprocess.PIPE,
        stderr=subprocess.DEVNULL,
        text=True,
    )
    assert process.stdout is not None
    for line in process.stdout:
        stripped = line.strip()
        if not stripped:
            continue
        print(json.dumps(render_payload(json.loads(stripped))), flush=True)


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print(json.dumps({"text": "󰂚!", "tooltip": str(exc), "class": "critical"}))
        sys.exit(1)
