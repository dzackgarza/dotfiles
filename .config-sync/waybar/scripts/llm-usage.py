#!/usr/bin/env python3
"""Waybar custom module: one provider's active 5h/7d usage windows.

Usage: llm-usage.py <provider-slug>
Consumes the usage-limits `--json` contract and emits one waybar JSON line.
"""
import json
import subprocess
import sys
from datetime import datetime, timezone

USAGE_LIMITS = "/home/dzack/gitclones/usage-limits/.venv/bin/usage-limits"

# Ayu Dark palette (matches waybar colors.css).
GREEN, YELLOW, RED, DIM = "#aad94c", "#ffb454", "#f07178", "#3e4b59"


def sev(pct):
    return RED if pct >= 100 else YELLOW if pct >= 80 else GREEN


def countdown(reset_at):
    """Reset timestamp -> 'in 2h21m', rounded to the nearest minute."""
    dt = datetime.fromisoformat(reset_at.replace("Z", "+00:00"))
    mins = max(0, round((dt - datetime.now(timezone.utc)).total_seconds() / 60))
    d, h, m = mins // 1440, mins % 1440 // 60, mins % 60
    parts = [f"{d}d" if d else "", f"{h}h" if d or h else "", f"{m}m"]
    return "".join(parts)


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
    # First ok snapshot with rows = the active account.
    snap = next((s for s in data["providers"] if s["status"] == "ok" and s["rows"]), None)
    if snap is None:
        print(json.dumps({"text": "—", "tooltip": f"{slug}: no active account", "class": "critical"}))
        return

    rows = {r["identifier"].rsplit("(", 1)[-1].rstrip(")"): r for r in snap["rows"]}
    h5, d7 = rows["5h"], rows["7d"]
    c5, c7 = h5["pct_used"], d7["pct_used"]
    worst = max(c5, c7)

    # Exhausted -> show a countdown to when the provider unblocks (latest
    # exhausted window's reset) instead of the percentages.
    blocked = [r for r in (h5, d7) if r["is_exhausted"]]
    if blocked:
        unblock = max(blocked, key=lambda r: r["reset_at"])
        text = f"<span color='{RED}'>{countdown(unblock['reset_at'])}</span>"
    else:
        text = (
            f"<span color='{sev(c5)}'>{c5}</span>"
            f"<span color='{DIM}'>/</span>"
            f"<span color='{sev(c7)}' size='smaller'>{c7}</span>"
        )
    tip = (
        f"{snap['display_name']} — {snap.get('account') or '?'}\n"
        f"  5h: {c5:>3}%  resets {h5['time_until_reset'] or 'n/a'}\n"
        f"  7d: {c7:>3}%  resets {d7['time_until_reset'] or 'n/a'}"
    )
    cls = "critical" if worst >= 100 else "warning" if worst >= 80 else ""
    print(json.dumps({"text": text, "tooltip": tip, "class": cls}))


if __name__ == "__main__":
    main()
