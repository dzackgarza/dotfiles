#!/usr/bin/env python3
import html
import json
import os
import re
import subprocess
import sys
import tempfile
from pathlib import Path

import yaml


def split_plan(plan_path: str) -> tuple[str, dict, str]:
    try:
        content = Path(plan_path).read_text(encoding="utf-8")
    except OSError:
        return "", {}, ""
    lines = content.splitlines(keepends=True)
    if not lines or lines[0].strip() != "---":
        return "", {}, content
    try:
        closing = next(i for i, line in enumerate(lines[1:], 1) if line.strip() == "---")
    except StopIteration:
        return "", {}, content
    raw = "".join(lines[1:closing]).rstrip("\n")
    try:
        metadata = yaml.safe_load(raw) or {}
    except yaml.YAMLError:
        metadata = {}
    if not isinstance(metadata, dict):
        metadata = {}
    return raw, metadata, "".join(lines[closing + 1 :])


def derive_vault(plan_path: str) -> str:
    parts = plan_path.split("/")
    if "projects" in parts:
        idx = parts.index("projects")
        if idx + 1 < len(parts):
            return parts[idx + 1]
    return ""




def find_checkout(repo: str) -> Path | None:
    repo_map = Path(__file__).resolve().parent.parent / "repo-map.json"
    try:
        payload = json.loads(repo_map.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        payload = {}
    entry = payload.get(repo) if isinstance(payload, dict) else None
    checkout = entry.get("checkout") if isinstance(entry, dict) else entry
    if isinstance(checkout, str) and checkout and checkout != "None":
        path = Path(checkout)
        if path.is_dir():
            return path
    return None


def humanize_work_id(node_id: str) -> str:
    special = {"api": "API", "sage": "Sage", "cas": "CAS", "gap": "GAP", "qc": "QC", "hom": "Hom"}
    return " ".join(special.get(word.lower(), word.capitalize()) for word in node_id.replace("-", " ").split())


def pending_work_records(checkout: Path | None) -> list[dict]:
    if checkout is None:
        return []
    todo = checkout / "TODO.md"
    if not todo.is_file():
        return []
    lines = todo.read_text(encoding="utf-8").splitlines()
    header = re.compile(r"^- \[([ x])\] \*\*`([^`]+)`\*\*\. \*\*Needs:\*\* (.*)$")
    records = []
    for index, line in enumerate(lines):
        match = header.match(line)
        if match is None or match.group(1) != " ":
            continue
        node_id = match.group(2)
        rest = match.group(3)
        needs_clause = rest.split(".", 1)[0]
        needs = [] if needs_clause.strip() == "none" else re.findall(r"`([^`]+)`", needs_clause)
        goal = ""
        cursor = index + 1
        while cursor < len(lines) and header.match(lines[cursor]) is None:
            goal_match = re.match(r"^\s+\*\*Goal:\*\*\s*(.+)$", lines[cursor])
            if goal_match:
                goal = goal_match.group(1).strip()
                break
            if lines[cursor].startswith("## "):
                break
            cursor += 1
        records.append({"id": node_id, "title": humanize_work_id(node_id), "goal": goal, "needs": needs, "optional": node_id.startswith("optional-")})
    open_ids = {record["id"] for record in records}
    for record in records:
        record["unmet"] = [need for need in record["needs"] if need in open_ids]
        record["state"] = "optional" if record["optional"] else ("waiting" if record["unmet"] else "ready")
    return records


def pending_work_markdown(repo: str) -> str:
    records = pending_work_records(find_checkout(repo))
    if not records:
        return ""
    groups = [("Ready now", "ready"), ("Waiting on pending prerequisites", "waiting"), ("Optional after required work", "optional")]
    chunks = ["## Pending execution work\n", "These are the repository's actual open dependency-DAG nodes, summarized at the mathematical/architectural goal level.\n"]
    for heading, state in groups:
        subset = [record for record in records if record["state"] == state]
        if not subset:
            continue
        chunks.append(f"### {heading}\n")
        for record in subset:
            needs = ", ".join(f"`{need}`" for need in record["needs"]) or "none"
            goal = record["goal"] or "No concise goal recorded."
            chunks.append(f"- **{record['title']}** (`{record['id']}`) — {goal}  \n  **Needs:** {needs}\n")
    return "\n".join(chunks) + "\n"

def combined_markdown(plan_paths: list[str], repo: str = "") -> str:
    chunks = ["# Current plans\n"]
    if repo:
        pending = pending_work_markdown(repo)
        if pending:
            chunks.append("\n" + pending)
    for plan_path in plan_paths:
        _raw, metadata, body = split_plan(plan_path)
        title = str(metadata.get("title") or Path(plan_path).stem)
        status = str(metadata.get("status") or "")
        description = str(metadata.get("description") or "").strip()
        chunks.append(f"\n## {title}\n")
        if description:
            chunks.append(
                f'\n<div class="plan-summary"><span class="plan-summary-label">Goal</span>{html.escape(description)}</div>\n'
            )
        if status:
            chunks.append(f"\n**Status:** `{status}`  \n")
        chunks.append(f"**Source:** `{plan_path}`\n\n")
        chunks.append(body.strip() + "\n")
    return "\n".join(chunks)


def parse_args() -> tuple[list[str], str, str, str, str]:
    if len(sys.argv) >= 2 and sys.argv[1] == "--plans-json":
        if len(sys.argv) != 6:
            raise SystemExit(f"Usage: {sys.argv[0]} --plans-json <json-path-list> <repo> <template> <out>")
        try:
            raw_paths = json.loads(sys.argv[2])
        except json.JSONDecodeError as exc:
            raise SystemExit(f"invalid plan path JSON: {exc}") from exc
        if not isinstance(raw_paths, list) or not raw_paths or not all(isinstance(path, str) and path for path in raw_paths):
            raise SystemExit("--plans-json requires a non-empty JSON array of plan paths")
        repo = sys.argv[3]
        template = sys.argv[4]
        out = sys.argv[5]
        vault = derive_vault(raw_paths[0])
        return raw_paths, repo, vault, template, out

    if len(sys.argv) < 3:
        raise SystemExit(f"Usage: {sys.argv[0]} <planPath> <repo> [vault] [template] [out]")
    plan_path = sys.argv[1]
    repo = sys.argv[2]
    vault = ""
    template = ""
    out = "/tmp/plan.html"
    if len(sys.argv) == 4:
        template = sys.argv[3]
    elif len(sys.argv) == 5:
        if sys.argv[3].endswith(".html") or ".template" in sys.argv[3]:
            template = sys.argv[3]
            out = sys.argv[4]
        else:
            vault = sys.argv[3]
            template = sys.argv[4]
    elif len(sys.argv) >= 6:
        vault = sys.argv[3]
        template = sys.argv[4]
        out = sys.argv[5]
    if not vault:
        vault = derive_vault(plan_path)
    return [plan_path], repo, vault, template, out


def main() -> None:
    plan_paths, repo, vault, template, out = parse_args()
    missing = [path for path in plan_paths if not os.path.isfile(path)]
    if missing:
        print(f"plan path does not exist: {missing[0]}", file=sys.stderr)
        raise SystemExit(2)

    raw_yaml = ""
    input_path = plan_paths[0]
    combined_path = ""
    if len(plan_paths) == 1:
        raw_yaml, _metadata, body = split_plan(plan_paths[0])
        pending = pending_work_markdown(repo)
        if pending:
            fd, combined_path = tempfile.mkstemp(suffix=".md", prefix="plan-with-pending-")
            with os.fdopen(fd, "w", encoding="utf-8") as combined:
                combined.write("---\n" + raw_yaml + "\n---\n")
                combined.write(pending + "\n" + body.lstrip())
            input_path = combined_path
    else:
        fd, combined_path = tempfile.mkstemp(suffix=".md", prefix="current-plans-")
        with os.fdopen(fd, "w", encoding="utf-8") as combined:
            combined.write(combined_markdown(plan_paths, repo))
        input_path = combined_path

    meta_fd, meta_path = tempfile.mkstemp(suffix=".yaml", prefix="plan-meta-")
    try:
        with os.fdopen(meta_fd, "w", encoding="utf-8") as mf:
            mf.write("---\n")
            if len(plan_paths) > 1:
                mf.write('title: "Current plans"\n')
                mf.write(f'subtitle: "{len(plan_paths)} active plan cards"\n')
            if raw_yaml:
                mf.write("yaml_raw: |\n")
                for line in raw_yaml.splitlines():
                    mf.write(f"  {line}\n")
            if repo:
                mf.write(f"repo: {json.dumps(repo)}\n")
            if vault:
                mf.write(f"vault: {json.dumps(vault)}\n")
            mf.write("...\n")
        args = ["pandoc", input_path, "--metadata-file", meta_path, "-s", "-o", out]
        if template and os.path.exists(template):
            args.extend(["--template", template])
        result = subprocess.run(args, capture_output=True, text=True)
        if result.returncode != 0:
            print(f"pandoc failed: {result.stderr}", file=sys.stderr)
            raise SystemExit(result.returncode)
        if raw_yaml and os.path.exists(out):
            try:
                html_content = Path(out).read_text(encoding="utf-8")
                escaped = html.escape(raw_yaml)
                pattern = r'<pre class="yaml-raw"><code>.*?</code></pre>'
                replacement = f'<pre class="yaml-raw"><code>{escaped}</code></pre>'
                new_html, count = re.subn(pattern, replacement, html_content, flags=re.DOTALL)
                if count:
                    Path(out).write_text(new_html, encoding="utf-8")
            except Exception as exc:
                print(f"post-process failed: {exc}", file=sys.stderr)
        rendered = ", ".join(plan_paths)
        print(f"Rendered {rendered} -> {out}")
    finally:
        try:
            os.remove(meta_path)
        except OSError:
            pass
        if combined_path:
            try:
                os.remove(combined_path)
            except OSError:
                pass


if __name__ == "__main__":
    main()
