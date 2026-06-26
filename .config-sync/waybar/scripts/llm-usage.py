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


def _window_label(row):
    return row["identifier"].rsplit("(", 1)[-1].rstrip(")")


def _is_spark(row):
    return "spark" in row["identifier"].lower()


def _line_for_row(label: str, row: dict | None) -> str:
    if row is None:
        return f"  {label:>7}:  n/a  resets n/a"
    return f"  {label:>7}: {row['pct_used']:>3}%  resets {row['time_until_reset'] or 'n/a'}"


def _pick_active_snapshot(providers: list[dict]) -> dict | None:
    candidates = [s for s in providers if s["status"] == "ok" and s["rows"]]
    if not candidates:
        return None

    default_snap = next((s for s in candidates if s.get("account") == "default"), None)
    if default_snap is not None:
        return default_snap

    ranked = [s for s in candidates if s.get("account")] or candidates
    return max(
        ranked,
        key=lambda s: s.get("metadata", {}).get("last_updated", ""),
    )


def _row_lookup(rows):
    by_window: dict[str, dict[str, dict]] = {}
    for row in rows:
        by_window.setdefault(_window_label(row), {})["spark" if _is_spark(row) else "main"] = row
    return by_window


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
    # Pick the active account snapshot from potentially multiple returned accounts.
    snap = _pick_active_snapshot(data["providers"])
    if snap is None:
        print(json.dumps({"text": "—", "tooltip": f"{slug}: no active account", "class": "critical"}))
        return

    rows_by_window = _row_lookup(snap["rows"])

    main5h = rows_by_window.get("5h", {}).get("main")
    main7d = rows_by_window.get("7d", {}).get("main")
    if main5h is None or main7d is None:
        print(
            json.dumps(
                {
                    "text": "—",
                    "tooltip": f"{slug}: missing usage rows",
                    "class": "critical",
                }
            )
        )
        return

    spark5h = rows_by_window.get("5h", {}).get("spark")
    spark7d = rows_by_window.get("7d", {}).get("spark")

    use_spark = (
        slug == "codex"
        and (main5h["is_exhausted"] or main7d["is_exhausted"])
        and spark5h is not None
        and spark7d is not None
    )

    if use_spark:
        h5 = spark5h
        d7 = spark7d
    else:
        h5 = main5h
        d7 = main7d

    c5, c7 = h5["pct_used"], d7["pct_used"]
    worst = max(c5, c7)

    # Exhausted -> show a countdown to when the displayed window unblocks
    # (latest exhausted window's reset) instead of percentages.
    blocked = [r for r in (h5, d7) if r["is_exhausted"]]
    show_countdown = bool(blocked)

    if blocked and show_countdown:
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
        + _line_for_row("5h", main5h)
        + "\n"
        + _line_for_row("7d", main7d)
        + "\n"
        + _line_for_row("Spark 5h", spark5h)
        + "\n"
        + _line_for_row("Spark 7d", spark7d)
    )
    cls = "critical" if worst >= 100 else "warning" if worst >= 80 else ""
    print(json.dumps({"text": text, "tooltip": tip, "class": cls}))


if __name__ == "__main__":
    main()
