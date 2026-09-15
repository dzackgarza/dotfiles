#!/usr/bin/env python3
import json
import os
import sys
from pathlib import Path

import yaml

vault_base = "/home/dzack/.agent-memory-vault/projects"

COMPLETE_STATUSES = {"complete", "done", "decided", "implemented"}
CURRENT_PLAN_STATUSES = {"in-progress"}
STATUS_ORDER = {"in-progress": 0}


def resolve_vault_path(repo_short: str) -> str | None:
    candidates = [
        f"github.com__dzackgarza__{repo_short}",
        f"github.com__dzackgarza__{repo_short.lower()}",
        repo_short,
        repo_short.lower(),
    ]
    if "/" in repo_short:
        short = repo_short.split("/")[-1]
        candidates.extend(
            [
                f"github.com__dzackgarza__{short}",
                f"github.com__dzackgarza__{short.lower()}",
                short,
                short.lower(),
            ]
        )
    for candidate in candidates:
        path = os.path.join(vault_base, candidate)
        if os.path.isdir(path):
            return path
    try:
        short = repo_short.split("/")[-1].lower()
        for entry in os.listdir(vault_base):
            if not entry.lower().endswith(f"__{short}"):
                continue
            if "dzackgarza" not in entry.lower() and repo_short.lower() not in entry.lower():
                continue
            path = os.path.join(vault_base, entry)
            if os.path.isdir(path):
                return path
    except OSError:
        pass
    return None


def frontmatter(path: Path) -> dict:
    try:
        text = path.read_text(encoding="utf-8")
        lines = text.splitlines()
        if not lines or lines[0].strip() != "---":
            return {}
        end = next(i for i, line in enumerate(lines[1:], 1) if line.strip() == "---")
        parsed = yaml.safe_load("\n".join(lines[1:end])) or {}
        return parsed if isinstance(parsed, dict) else {}
    except (OSError, UnicodeError, yaml.YAMLError, StopIteration):
        return {}


def todo_counts(metadata: dict) -> tuple[int, int]:
    todos = metadata.get("todos")
    if not isinstance(todos, list):
        return (0, 0)
    total = 0
    completed = 0
    for todo in todos:
        if not isinstance(todo, dict):
            continue
        total += 1
        if str(todo.get("status", "")) in COMPLETE_STATUSES:
            completed += 1
    return total, completed


def structured_plan_records(vault_path: str) -> list[dict]:
    plans_root = Path(vault_path) / "plans"
    if not plans_root.is_dir():
        return []
    records: list[dict] = []
    for path in sorted(plans_root.rglob("PLAN-*.md")):
        metadata = frontmatter(path)
        card_id = metadata.get("id")
        if not isinstance(card_id, str) or not card_id.startswith("PLAN-"):
            # Legacy note-style plans are historical records, not structured plan cards.
            continue
        archived = metadata.get("archived", False) is True
        status = str(metadata.get("status", ""))
        title = str(metadata.get("title", card_id))
        total, completed = todo_counts(metadata)
        records.append(
            {
                "id": card_id,
                "title": title,
                "status": status,
                "archived": archived,
                "path": str(path),
                "todos": total,
                "completedTodos": completed,
            }
        )
    return records


def summarize(vault_path: str) -> dict:
    records = structured_plan_records(vault_path)
    visible = [record for record in records if not record["archived"]]
    current = [record for record in visible if record["status"] in CURRENT_PLAN_STATUSES]
    current.sort(key=lambda record: (STATUS_ORDER.get(record["status"], 99), record["title"].lower()))

    todo_records = [record for record in current if record["todos"] > 0]
    if todo_records:
        total = sum(record["todos"] for record in todo_records)
        completed = sum(record["completedTodos"] for record in todo_records)
    else:
        total = len(visible)
        completed = sum(1 for record in visible if record["status"] in COMPLETE_STATUSES)
    percent = int(completed * 100 / total) if total else 0

    active_plans = []
    for record in current:
        plan = {
            "title": record["title"],
            "path": record["path"],
            "status": record["status"],
            "total": record["todos"],
            "completed": record["completedTodos"],
        }
        plan["percent"] = int(record["completedTodos"] * 100 / record["todos"]) if record["todos"] else 0
        active_plans.append(plan)

    if not active_plans:
        active_label = "No plan active"
        active_path = ""
    elif len(active_plans) == 1:
        active_label = active_plans[0]["title"]
        active_path = active_plans[0]["path"]
    else:
        active_label = f"{len(active_plans)} current plans"
        active_path = active_plans[0]["path"]

    return {
        "total": total,
        "completed": completed,
        "percent": percent,
        "activePlan": active_label,
        "activePlanPath": active_path,
        "activePlans": active_plans,
    }


def empty_result() -> dict:
    return {
        "total": 0,
        "completed": 0,
        "percent": 0,
        "vault": "No vault initialized",
        "activePlan": "No plan active",
        "activePlanPath": "",
        "activePlans": [],
    }


def get_progress(repo_short: str) -> None:
    vault_path = resolve_vault_path(repo_short)
    if not vault_path:
        print(json.dumps(empty_result()))
        return
    result = summarize(vault_path)
    result["vault"] = os.path.basename(vault_path)
    print(json.dumps(result))


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(json.dumps(empty_result()))
    else:
        get_progress(sys.argv[1])
