#!/usr/bin/env python3
"""Compact Hyprland workspace summary for Waybar."""

import html
import json
import subprocess
from pathlib import Path


HYPRCTL = Path("/bin/hyprctl")
PERSISTENT_WORKSPACE_IDS = tuple(range(1, 11))

FG = "#cdd6f4"
DIM = "#3e4b59"
ACTIVE_FG = "#11111b"
ACTIVE_BG = "#cdd6f4"
COUNT = "#ffb454"
SEPARATOR = "│"


def _workspace_ids(workspaces: list[dict]) -> list[int]:
    ids = set(PERSISTENT_WORKSPACE_IDS)
    ids.update(workspace["id"] for workspace in workspaces if workspace["id"] > 0)
    return sorted(ids)


def _workspace_item(workspace_id: int, windows: int, active_id: int) -> str:
    count = ""
    if windows > 0:
        count = f"<span foreground='{COUNT}' size='xx-small' rise='6500'>{windows}</span>"
    if workspace_id == active_id:
        return (
            f"<span foreground='{ACTIVE_FG}' background='{ACTIVE_BG}'>{workspace_id}</span>"
            f"{count}"
        )
    if windows == 0:
        return f"<span foreground='{DIM}'>{workspace_id}</span>"
    return f"<span foreground='{FG}'>{workspace_id}</span>{count}"


def render_payload(workspaces: list[dict], active_workspace: dict) -> dict:
    by_id = {workspace["id"]: workspace for workspace in workspaces if workspace["id"] > 0}
    active_id = active_workspace["id"]
    items = []
    tooltip_lines = []

    for workspace_id in _workspace_ids(workspaces):
        workspace = by_id.get(workspace_id, {})
        windows = int(workspace.get("windows", 0))
        monitor = workspace.get("monitor", "?")
        active_prefix = "* " if workspace_id == active_id else "  "
        items.append(_workspace_item(workspace_id, windows, active_id))
        tooltip_lines.append(f"{active_prefix}{workspace_id}: {windows} windows ({monitor})")

    return {
        "text": f"<span foreground='{DIM}'> {SEPARATOR} </span>".join(items),
        "tooltip": "\n".join(tooltip_lines),
        "class": "compact-workspaces",
    }


def _hyprctl_json(*args: str):
    assert HYPRCTL.is_file(), f"hyprctl is required at {HYPRCTL}"
    output = subprocess.check_output([HYPRCTL, *args, "-j"], text=True)
    return json.loads(output)


def main() -> None:
    try:
        payload = render_payload(
            _hyprctl_json("workspaces"),
            _hyprctl_json("activeworkspace"),
        )
    except Exception as exc:
        payload = {
            "text": "ws:err",
            "tooltip": str(exc),
            "class": "critical",
        }
    print(json.dumps(payload))


if __name__ == "__main__":
    main()
