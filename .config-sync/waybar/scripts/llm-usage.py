#!/usr/bin/env python3
"""Waybar custom module: provider active 5h/7d usage windows.

Usage: llm-usage.py <provider-slug>
Consumes the usage-limits `--json` contract and emits one waybar JSON line.
"""
import json
import os
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

USAGE_LIMITS = "/home/dzack/gitclones/usage-limits/.venv/bin/usage-limits"

# Ayu Dark palette (matches waybar colors.css).
GREEN, YELLOW, RED, DIM = "#aad94c", "#ffb454", "#f07178", "#3e4b59"
REGULAR_ICON, SPARK_ICON = "●", "⚡"

# Fresh-window "touch": call the model with a trivial prompt so the rolling 5h
# window starts ticking the moment it opens. ponytail: 4.5h cooldown assumes 5h
# windows — bump if the window length changes.
STATE_DIR = Path(os.environ.get("XDG_CACHE_HOME", os.path.expanduser("~/.cache"))) / "waybar-llm-usage"
TOUCH_COOLDOWN = 4.5 * 3600
TOUCH_TIMEOUT = "45"  # seconds, passed to timeout(1)
TOUCH_CMDS = {
    "claude": ["claude", "-p", "Reply with exactly: Ok"],
    "codex": ["codex", "exec", "--skip-git-repo-check", "-s", "read-only", "Reply with exactly: Ok"],
}


def sev(pct):
    return RED if pct >= 100 else YELLOW if pct >= 80 else GREEN


def countdown(reset_at, now=None):
    """Reset timestamp -> compact remaining time; minutes when <= 1h, else tenths of an hour."""
    dt = datetime.fromisoformat(reset_at.replace("Z", "+00:00"))
    current = now or datetime.now(timezone.utc)
    seconds = max(0, (dt - current).total_seconds())
    if seconds <= 3600:
        return f"{round(seconds / 60)}m"
    return f"{seconds / 3600:.1f}h"


def _window_label(row):
    return row["identifier"].rsplit("(", 1)[-1].rstrip(")")


def _is_spark(row):
    return "spark" in row["identifier"].lower()


def _line_for_row(label: str, row: dict | None) -> str:
    if row is None:
        return f"  {label:>7}:  n/a  resets n/a"
    return f"  {label:>7}: {row['pct_used']:>3}%  resets {row['time_until_reset'] or 'n/a'}"


def _active_snapshots(slug: str, providers: list[dict]) -> list[dict]:
    snapshots = [
        snapshot
        for snapshot in providers
        if snapshot["provider"] == slug and snapshot["status"] == "ok" and snapshot["rows"]
    ]
    return sorted(snapshots, key=lambda snapshot: snapshot.get("account") or snapshot["display_name"])


def _compact_item(icon: str, icon_color: str, rows: list[dict]) -> tuple[str, int]:
    if not rows:
        return f"<span color='{icon_color}'>{icon}</span><span color='{DIM}'>n/a</span>", 0

    blocked = [r for r in rows if r["is_exhausted"]]

    if blocked:
        nearest_reset = min(blocked, key=lambda r: r["reset_at"])
        body = f"<span color='{RED}'>{countdown(nearest_reset['reset_at'])}</span>"
        worst = 100
    else:
        parts = []
        worst = 0
        for i, r in enumerate(rows):
            pct = r["pct_used"]
            if i == 0:
                parts.append(f"<span color='{sev(pct)}'>{pct}</span>")
            else:
                parts.append(f"<span color='{sev(pct)}' size='smaller'>{pct}</span>")
            worst = max(worst, pct)
        body = f"<span color='{DIM}'>/</span>".join(parts)

    return f"<span color='{icon_color}'>{icon}</span>{body}", worst


def _snapshot_payload(slug: str, snap: dict) -> tuple[str, str, int]:
    main_rows = [r for r in snap["rows"] if not _is_spark(r)]
    spark_rows = [r for r in snap["rows"] if _is_spark(r)]

    rendered_items = [_compact_item(REGULAR_ICON, DIM, main_rows)]
    if spark_rows:
        rendered_items.append(_compact_item(SPARK_ICON, YELLOW, spark_rows))

    text = f"<span color='{DIM}'> </span>".join(item[0] for item in rendered_items)
    worst = max(item[1] for item in rendered_items)

    lines = [f"{snap['display_name']} - {snap.get('account') or '?'}"]
    for r in snap["rows"]:
        lines.append(f"  {r['identifier']:>15}: {r['pct_used']:>3}%  resets {r['time_until_reset'] or 'n/a'}")
    tip = "\n".join(lines)
    return text, tip, worst


def render_waybar_payload(slug: str, data: dict) -> dict:
    snapshots = _active_snapshots(slug, data["providers"])
    if not snapshots:
        return {"text": "-", "tooltip": f"{slug}: no active account", "class": "critical"}

    rendered = [_snapshot_payload(slug, snapshot) for snapshot in snapshots]
    worst = max(row[2] for row in rendered)
    cls = "critical" if worst >= 100 else "warning" if worst >= 80 else ""
    return {
        "text": f"<span color='{DIM}'> | </span>".join(row[0] for row in rendered),
        "tooltip": "\n\n".join(row[1] for row in rendered),
        "class": cls,
    }


def _fresh_window_ready(slug: str, data: dict) -> bool:
    """A main window is open, not exhausted, and at 0% -- i.e. just reset/untouched."""
    for snap in _active_snapshots(slug, data["providers"]):
        for r in snap["rows"]:
            if not _is_spark(r) and not r["is_exhausted"] and r["pct_used"] == 0:
                return True
    return False


def maybe_touch_fresh_window(slug: str, data: dict, now=None) -> None:
    """On a freshly reset window, notify and fire a trivial model call to start the timer."""
    cmd = TOUCH_CMDS.get(slug)
    if cmd is None or not _fresh_window_ready(slug, data):
        return


    STATE_DIR.mkdir(parents=True, exist_ok=True)
    marker = STATE_DIR / f"{slug}.touched"
    current = now if now is not None else time.time()
    try:
        if current - marker.stat().st_mtime < TOUCH_COOLDOWN:
            return  # already touched this window
    except FileNotFoundError:
        pass
    marker.touch()

    subprocess.Popen(["notify-send", "LLM window reset", f"Touching {slug} to start the 5h timer"])
    # Detached + hard timeout so a hung harness never blocks the waybar poll.
    subprocess.Popen(
        ["timeout", TOUCH_TIMEOUT, *cmd],
        stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
        start_new_session=True,
    )


def main():
    slug = sys.argv[1]
    out = subprocess.run(
        [USAGE_LIMITS, "--json", "-p", slug],
        capture_output=True, text=True, timeout=90,
    )
    if out.returncode != 0:
        print(json.dumps({"text": "err", "tooltip": out.stderr.strip(), "class": "critical"}))
        return

    data = json.loads(out.stdout)
    maybe_touch_fresh_window(slug, data)
    print(json.dumps(render_waybar_payload(slug, data)))


if __name__ == "__main__":
    main()
