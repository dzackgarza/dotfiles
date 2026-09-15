#!/usr/bin/env python3
"""Render the canonical active agent-memory DAG as self-contained HTML.

The renderer intentionally does not reconstruct graph structure by scanning every plan file:
`agent-memory plan dag --visibility active` already owns that projection in plan-dag.md.
It also does not require browser-side graph libraries or network access; Graphviz produces
SVG at render time so file:// inspection is reliable offline.
"""
from __future__ import annotations

import html
import json
import os
import re
import subprocess
import sys
from pathlib import Path
from typing import Any

import yaml

VAULT_BASE = Path("/home/dzack/.agent-memory-vault/projects")
DEFAULT_TEMPLATE = Path("/home/dzack/dotfiles/ags/control-panel/templates/dag.html")

STATUS_STYLE = {
    "complete": ("#dcfce7", "#22c55e"),
    "in-progress": ("#fef9c3", "#eab308"),
    "blocked": ("#fee2e2", "#ef4444"),
    "needs-agent-review": ("#ffedd5", "#f97316"),
    "needs-human-input": ("#ffedd5", "#f97316"),
    "approved-and-unstarted": ("#f4f4f5", "#a1a1aa"),
    "unstarted": ("#f4f4f5", "#a1a1aa"),
}


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
    if not text.startswith("---"):
        return {}
    match = re.match(r"^---\s*\n(.*?)\n---\s*(?:\n|$)", text, re.DOTALL)
    if match is None:
        return {}
    try:
        payload = yaml.safe_load(match.group(1)) or {}
    except yaml.YAMLError:
        return {}
    return payload if isinstance(payload, dict) else {}


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
        records[card_id] = meta
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
            continue
        # agent-memory emits bare card ids for isolated nodes.
        if re.fullmatch(r"[^\s]+", line):
            add_node(line)
    return nodes, edges


def dot_quote(value: str) -> str:
    return json.dumps(value, ensure_ascii=False)


def wrapped_label(value: str, width: int = 30) -> str:
    words = value.split()
    lines: list[str] = []
    current: list[str] = []
    length = 0
    for word in words:
        extra = len(word) + (1 if current else 0)
        if current and length + extra > width:
            lines.append(" ".join(current))
            current = [word]
            length = len(word)
        else:
            current.append(word)
            length += extra
    if current:
        lines.append(" ".join(current))
    return "\\n".join(lines) if lines else value


def graphviz_svg(
    nodes: list[str],
    edges: list[tuple[str, str]],
    metadata: dict[str, dict[str, Any]],
    *,
    edge_color: str,
) -> str:
    lines = [
        "digraph G {",
        '  graph [rankdir=LR, bgcolor="transparent", pad="0.25", nodesep="0.28", ranksep="0.55", splines=ortho];',
        '  node [fontname="Inter, sans-serif", fontsize=10, margin="0.12,0.08", style="rounded,filled", penwidth=1.2];',
        f'  edge [color="{edge_color}", penwidth=1.2, arrowsize=0.7];',
    ]
    for node_id in nodes:
        meta = metadata.get(node_id, {})
        title = str(meta.get("title") or node_id)
        status = str(meta.get("status") or "unknown")
        fill, stroke = STATUS_STYLE.get(status, ("#f9fafb", "#9ca3af"))
        if node_id.startswith("FEATURE-"):
            shape = "ellipse"
        elif node_id.startswith("PC-"):
            shape = "note"
        else:
            shape = "box"
        tooltip = f"{title} [{status}]"
        lines.append(
            "  "
            + dot_quote(node_id)
            + " ["
            + ", ".join(
                [
                    f"label={dot_quote(wrapped_label(title))}",
                    f"tooltip={dot_quote(tooltip)}",
                    f"shape={shape}",
                    f"fillcolor={dot_quote(fill)}",
                    f"color={dot_quote(stroke)}",
                ]
            )
            + "];"
        )
    for source, target in edges:
        lines.append(f"  {dot_quote(source)} -> {dot_quote(target)};")
    lines.append("}")
    dot_source = "\n".join(lines)
    result = subprocess.run(
        ["dot", "-Tsvg"],
        input=dot_source,
        text=True,
        capture_output=True,
        check=False,
    )
    if result.returncode != 0:
        raise RuntimeError(f"Graphviz failed: {result.stderr.strip()}")
    svg = re.sub(r"<\?xml.*?\?>\s*", "", result.stdout, flags=re.DOTALL)
    svg = re.sub(r"<!DOCTYPE.*?>\s*", "", svg, flags=re.DOTALL)
    svg = svg.replace("<svg ", '<svg class="dag-svg" ', 1)
    return svg


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

    dep_svg = graphviz_svg(dep_nodes, dep_edges, metadata, edge_color="#94a3b8")
    containment_svg = graphviz_svg(
        containment_nodes, containment_edges, metadata, edge_color="#c4b5fd"
    )

    template_path = template_arg if template_arg and template_arg.is_file() else DEFAULT_TEMPLATE
    template = template_path.read_text(encoding="utf-8")
    vault_name = vault_path.name
    replacements = {
        "__VAULT__": html.escape(vault_name),
        "__REPO__": html.escape(repo),
        "__DEPENDENCIES_SVG__": dep_svg,
        "__CONTAINMENT_SVG__": containment_svg,
        "__DEPENDENCY_STATS__": f"{len(dep_nodes)} nodes · {len(dep_edges)} edges",
        "__CONTAINMENT_STATS__": f"{len(containment_nodes)} nodes · {len(containment_edges)} edges",
        "__SOURCE_PATH__": html.escape(str(dag_path)),
    }
    rendered = template
    for key, value in replacements.items():
        rendered = rendered.replace(key, value)

    if out is None:
        out = Path("/tmp") / f"{vault_name.replace('/', '-')}-dag.html"
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
        # Existing AGS caller passes the template as the second argument.
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
