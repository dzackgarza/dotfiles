#!/usr/bin/env python3
"""Waybar notification indicator backed by swaync-client."""

import json
import subprocess
import sys
from pathlib import Path


SWAYNC_CLIENT = Path("/bin/swaync-client")
BELL = "󰂚"
BELL_OFF = "󰂛"
COUNT = "#ffb454"


def render_payload(status: dict) -> dict:
    text = str(status.get("text") or "").strip()
    alt = str(status.get("alt") or "")
    css_class = status.get("class") or alt or "none"
    dnd = "dnd" in alt or "dnd" in str(css_class)
    icon = BELL_OFF if dnd else BELL
    count = ""
    if text and text != "0":
        count = f"<span foreground='{COUNT}' size='x-small' rise='4500'>{text}</span>"
    return {
        "text": f"{icon}{count}",
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
