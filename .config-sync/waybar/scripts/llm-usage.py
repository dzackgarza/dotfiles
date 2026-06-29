#!/usr/bin/env python3
"""Waybar custom module: provider active 5h/7d usage windows.

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
REGULAR_ICON, SPARK_ICON = "●", "⚡"


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


def _active_snapshots(slug: str, providers: list[dict]) -> list[dict]:
    snapshots = [
        snapshot
        for snapshot in providers
        if snapshot["provider"] == slug and snapshot["status"] == "ok" and snapshot["rows"]
    ]
    return sorted(snapshots, key=lambda snapshot: snapshot.get("account") or snapshot["display_name"])


def _row_lookup(rows):
    by_window: dict[str, dict[str, dict]] = {}
    for row in rows:
        by_window.setdefault(_window_label(row), {})["spark" if _is_spark(row) else "main"] = row
    return by_window


def _display_rows(slug: str, rows_by_window: dict[str, dict[str, dict]]) -> tuple[dict, dict]:
    main5h = rows_by_window.get("5h", {}).get("main")
    main7d = rows_by_window.get("7d", {}).get("main")
    assert main5h is not None and main7d is not None, (
        f"{slug}: usage-limits provider snapshot is missing required main windows; "
        f"found windows={sorted(rows_by_window)}; fix usage-limits provider rows"
    )

    return main5h, main7d


def _compact_item(icon: str, icon_color: str, h5: dict, d7: dict) -> tuple[str, int]:
    c5, c7 = h5["pct_used"], d7["pct_used"]
    worst = max(c5, c7)
    blocked = [r for r in (h5, d7) if r["is_exhausted"]]

    if blocked:
        nearest_reset = min(blocked, key=lambda r: r["reset_at"])
        body = f"<span color='{RED}'>{countdown(nearest_reset['reset_at'])}</span>"
    else:
        body = (
            f"<span color='{sev(c5)}'>{c5}</span>"
            f"<span color='{DIM}'>/</span>"
            f"<span color='{sev(c7)}' size='smaller'>{c7}</span>"
        )

    return f"<span color='{icon_color}'>{icon}</span>{body}", worst


def _snapshot_payload(slug: str, snap: dict) -> tuple[str, str, int]:
    rows_by_window = _row_lookup(snap["rows"])
    main5h = rows_by_window.get("5h", {}).get("main")
    main7d = rows_by_window.get("7d", {}).get("main")
    h5, d7 = _display_rows(slug, rows_by_window)
    spark5h = rows_by_window.get("5h", {}).get("spark")
    spark7d = rows_by_window.get("7d", {}).get("spark")
    rendered_items = [_compact_item(REGULAR_ICON, DIM, h5, d7)]
    if spark5h is not None and spark7d is not None:
        rendered_items.append(_compact_item(SPARK_ICON, YELLOW, spark5h, spark7d))

    text = f"<span color='{DIM}'> </span>".join(item[0] for item in rendered_items)
    worst = max(item[1] for item in rendered_items)
    tip = (
        f"{snap['display_name']} - {snap.get('account') or '?'}\n"
        + _line_for_row("5h", main5h)
        + "\n"
        + _line_for_row("7d", main7d)
        + "\n"
        + _line_for_row("Spark 5h", spark5h)
        + "\n"
        + _line_for_row("Spark 7d", spark7d)
    )
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
    print(json.dumps(render_waybar_payload(slug, data)))


if __name__ == "__main__":
    main()
