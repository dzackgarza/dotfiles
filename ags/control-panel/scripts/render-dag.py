#!/usr/bin/env python3
"""Render the canonical active agent-memory plan graph as an interactive HTML dashboard.

Graph structure comes from the validated `plans/plan-dag.md` projection.  D3 and d3-dag
remain browser-side because the dashboard is interactive; their declared local package
assets are embedded into the generated file so `file://` inspection is deterministic and
does not depend on CDN availability.
"""
from __future__ import annotations

import html
import json
import re
import sys
from pathlib import Path
from typing import Any

import yaml

VAULT_BASE = Path("/home/dzack/.agent-memory-vault/projects")
CONTROL_PANEL_ROOT = Path(__file__).resolve().parent.parent
AGS_ROOT = CONTROL_PANEL_ROOT.parent
DEFAULT_TEMPLATE = CONTROL_PANEL_ROOT / "templates" / "dag.html"
D3_JS = AGS_ROOT / "node_modules" / "d3" / "dist" / "d3.min.js"
D3_DAG_JS = AGS_ROOT / "node_modules" / "d3-dag" / "bundle" / "d3-dag.iife.min.js"


def find_vault(repo_short: str) -> Path | None:
    short = repo_short.split("/")[-1]
    candidates = [
        f"github.com__dzackgarza__{repo_short}",
        f"github.com__dzackgarza__{repo_short.lower()}",
        f"github.com__dzackgarza__{short}",
        f"github.com__dzackgarza__{short.lower()}",
        repo_short,
        repo_short.lower(),
        short,
        short.lower(),
    ]
    for candidate in candidates:
        path = VAULT_BASE / candidate
        if path.is_dir():
            return path
    if VAULT_BASE.is_dir():
        suffix = f"__{short.lower()}"
        for path in VAULT_BASE.iterdir():
            if path.is_dir() and path.name.lower().endswith(suffix):
                return path
    return None


def read_frontmatter(path: Path) -> dict[str, Any]:
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return {}
    match = re.match(r"^---\s*\n(.*?)\n---\s*(?:\n|$)", text, re.DOTALL)
    if match is None:
        return {}
    try:
        payload = yaml.safe_load(match.group(1)) or {}
    except yaml.YAMLError:
        return {}
    return payload if isinstance(payload, dict) else {}


def todo_counts(meta: dict[str, Any]) -> tuple[int, int]:
    todos = meta.get("todos")
    if not isinstance(todos, list):
        return 0, 0
    total = 0
    completed = 0
    stack = list(todos)
    while stack:
        todo = stack.pop()
        if not isinstance(todo, dict):
            continue
        total += 1
        if todo.get("status") == "complete":
            completed += 1
        children = todo.get("children")
        if isinstance(children, list):
            stack.extend(children)
    return completed, total


def active_card_metadata(vault_path: Path) -> dict[str, dict[str, Any]]:
    plans_root = vault_path / "plans"
    records: dict[str, dict[str, Any]] = {}
    if not plans_root.is_dir():
        return records
    for path in plans_root.rglob("*.md"):
        if path.name in {"plan-dag.md", "plan-dag-archived.md"}:
            continue
        meta = read_frontmatter(path)
        card_id = meta.get("id")
        if not isinstance(card_id, str) or meta.get("archived") is True:
            continue
        complete, total = todo_counts(meta)
        records[card_id] = {
            **meta,
            "path": str(path),
            "todo_completed": complete,
            "todo_total": total,
        }
    return records


def mermaid_section(source: str, heading: str) -> str:
    pattern = rf"^## {re.escape(heading)}\s*$.*?```mermaid\s*\n(.*?)```"
    match = re.search(pattern, source, re.MULTILINE | re.DOTALL)
    return match.group(1) if match else ""


def parse_mermaid_graph(block: str) -> tuple[list[str], list[tuple[str, str]]]:
    nodes: list[str] = []
    seen: set[str] = set()
    edges: list[tuple[str, str]] = []

    def add_node(node_id: str) -> None:
        if node_id and node_id not in seen:
            seen.add(node_id)
            nodes.append(node_id)

    for raw in block.splitlines():
        line = raw.strip()
        if not line or line.startswith("graph ") or line.startswith("%%"):
            continue
        edge_match = re.fullmatch(r"([^\s]+)\s*-->\s*([^\s]+)", line)
        if edge_match:
            source, target = edge_match.groups()
            add_node(source)
            add_node(target)
            edges.append((source, target))
        elif re.fullmatch(r"[^\s]+", line):
            add_node(line)
    return nodes, edges


def node_payload(node_id: str, metadata: dict[str, dict[str, Any]]) -> dict[str, Any]:
    meta = metadata.get(node_id, {})
    title = str(meta.get("title") or node_id)
    status = str(meta.get("status") or "unknown")
    description = str(meta.get("description") or "").strip()
    completed = int(meta.get("todo_completed") or 0)
    total = int(meta.get("todo_total") or 0)
    if node_id.startswith("FEATURE-"):
        kind = "feature"
    elif node_id.startswith("PLAN-"):
        kind = "plan"
    elif node_id.startswith("PC-"):
        kind = "checkpoint"
    else:
        kind = "card"
    return {
        "id": node_id,
        "label": title,
        "title": title,
        "description": description,
        "status": status,
        "kind": kind,
        "path": str(meta.get("path") or ""),
        "todoCompleted": completed,
        "todoTotal": total,
    }


def graph_payload(
    nodes: list[str], edges: list[tuple[str, str]], metadata: dict[str, dict[str, Any]]
) -> dict[str, Any]:
    return {
        "nodes": [node_payload(node_id, metadata) for node_id in nodes],
        "edges": [{"from": source, "to": target} for source, target in edges],
    }


def read_browser_asset(path: Path, label: str) -> str:
    if not path.is_file():
        raise SystemExit(
            f"Missing local {label} asset at {path}. Run the AGS dependency install before rendering the DAG."
        )
    return path.read_text(encoding="utf-8")


def render(repo: str, out: Path | None, template_arg: Path | None) -> Path:
    vault_path = find_vault(repo)
    if vault_path is None:
        raise SystemExit(f"Vault not found for {repo}")
    dag_path = vault_path / "plans" / "plan-dag.md"
    if not dag_path.is_file():
        raise SystemExit(
            f"Active DAG not found at {dag_path}; regenerate it with agent-memory plan dag --visibility active"
        )

    source = dag_path.read_text(encoding="utf-8")
    metadata = active_card_metadata(vault_path)
    dep_nodes, dep_edges = parse_mermaid_graph(mermaid_section(source, "Dependencies"))
    containment_nodes, containment_edges = parse_mermaid_graph(
        mermaid_section(source, "Containment")
    )
    if not dep_nodes and not containment_nodes:
        raise SystemExit(f"No graph nodes found in canonical DAG {dag_path}")

    graphs = {
        "dependencies": graph_payload(dep_nodes, dep_edges, metadata),
        "containment": graph_payload(containment_nodes, containment_edges, metadata),
    }
    template_path = template_arg if template_arg and template_arg.is_file() else DEFAULT_TEMPLATE
    template = template_path.read_text(encoding="utf-8")
    replacements = {
        "__VAULT__": html.escape(vault_path.name),
        "__REPO__": html.escape(repo),
        "__SOURCE_PATH__": html.escape(str(dag_path)),
        "__GRAPHS_JSON__": json.dumps(graphs, ensure_ascii=False).replace("</", "<\\/"),
        "__D3_JS__": read_browser_asset(D3_JS, "D3"),
        "__D3_DAG_JS__": read_browser_asset(D3_DAG_JS, "d3-dag"),
    }
    rendered = template
    for key, value in replacements.items():
        rendered = rendered.replace(key, value)

    if out is None:
        out = Path("/tmp") / f"{vault_path.name.replace('/', '-')}-dag.html"
    out.write_text(rendered, encoding="utf-8")
    return out


def main() -> None:
    if len(sys.argv) < 2:
        raise SystemExit(f"Usage: {sys.argv[0]} <repoOrVault> [out.html] [template.html]")
    repo = sys.argv[1]
    out: Path | None = None
    template: Path | None = None
    if len(sys.argv) == 3:
        candidate = Path(sys.argv[2])
        if candidate.name == "dag.html" or "template" in candidate.name:
            template = candidate
        else:
            out = candidate
    elif len(sys.argv) >= 4:
        if sys.argv[2]:
            out = Path(sys.argv[2])
        if sys.argv[3]:
            template = Path(sys.argv[3])
    print(render(repo, out, template))


if __name__ == "__main__":
    main()
