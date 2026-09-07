#!/usr/bin/env python3
import json
import os
import re
import subprocess
import sys

vault_base = "/home/dzack/.agent-memory-vault/projects"


def find_vault(repo_short):
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
    vault_path = None
    for cand in candidates:
        p = os.path.join(vault_base, cand)
        if os.path.isdir(p):
            vault_path = p
            break
    if not vault_path:
        try:
            for entry in os.listdir(vault_base):
                if entry.lower().endswith(f"__{repo_short.split('/')[-1].lower()}"):
                    if (
                        "dzackgarza" in entry.lower()
                        or repo_short.lower() in entry.lower()
                    ):
                        maybe = os.path.join(vault_base, entry)
                        if os.path.isdir(maybe):
                            vault_path = maybe
                            break
        except:
            pass
    return vault_path


def parse_frontmatter(path):
    try:
        with open(path, "r", encoding="utf-8") as f:
            content = f.read()
        # Extract YAML between first --- and second ---
        m = re.search(r"^---\s*\n(.*?)\n---\s*\n", content, re.DOTALL | re.MULTILINE)
        if not m:
            return {}
        yaml_text = m.group(1)
        # Try yaml lib if available
        try:
            import yaml

            data = yaml.safe_load(yaml_text)
            if isinstance(data, dict):
                return data
        except:
            pass
        # Fallback regex parse for key fields
        data = {}
        # id
        m_id = re.search(r"^id:\s*(.+)$", yaml_text, re.MULTILINE)
        if m_id:
            data["id"] = m_id.group(1).strip().strip("'\"")
        # title
        m_title = re.search(r"^title:\s*(.+)$", yaml_text, re.MULTILINE)
        if m_title:
            # Handle multiline title? Take first line and strip
            data["title"] = m_title.group(1).strip().strip("'\"")
            # If title is quoted and multiline, the above may capture only first line; try to handle
            # For simplicity, if title line ends with no closing quote and next line is indented, join
            # But for now, just use first line
        # status
        m_status = re.search(r"^status:\s*(.+)$", yaml_text, re.MULTILINE)
        if m_status:
            data["status"] = m_status.group(1).strip().strip("'\"")
        # parents - extract list
        # Look for parents: followed by list items
        m_parents = re.search(
            r"^parents:\s*\n((?:\s*-\s*.+\n?)+)", yaml_text, re.MULTILINE
        )
        if m_parents:
            block = m_parents.group(1)
            parents = []
            for line in block.splitlines():
                mm = re.search(r"-\s*(.+)", line)
                if mm:
                    val = mm.group(1).strip().strip("'\"")
                    # Clean [[...]]
                    val = val.strip()
                    # Remove surrounding [[ and ]]
                    if val.startswith("[[") and val.endswith("]]"):
                        val = val[2:-2]
                    # Remove any remaining brackets/quotes
                    val = val.strip("'\"")
                    parents.append(val)
            data["parents"] = parents
        else:
            # Try inline list: parents: ['...', '...']
            m_parents_inline = re.search(
                r"^parents:\s*\[(.+)\]", yaml_text, re.MULTILINE
            )
            if m_parents_inline:
                inner = m_parents_inline.group(1)
                parts = re.split(r",", inner)
                parents = [p.strip().strip("'\" ").strip() for p in parts if p.strip()]
                # Clean [[ ]]
                cleaned = []
                for p in parents:
                    if p.startswith("[[") and p.endswith("]]"):
                        p = p[2:-2]
                    cleaned.append(p)
                data["parents"] = cleaned
        return data
    except Exception:
        return {}


def main():
    if len(sys.argv) < 2:
        print(
            f"Usage: {sys.argv[0]} <repoOrVault> [out.html] [template.html]",
            file=sys.stderr,
        )
        sys.exit(1)
    repo = sys.argv[1]
    out = sys.argv[2] if len(sys.argv) > 2 else None
    template_arg = sys.argv[3] if len(sys.argv) > 3 else None

    vault_path = find_vault(repo)
    vault_name = os.path.basename(vault_path) if vault_path else repo.replace("/", "__")
    if not vault_path or not os.path.isdir(vault_path):
        print(f"Vault not found for {repo}, using empty DAG", file=sys.stderr)
        vault_path = None

    nodes = []
    edges = []
    id_to_title = {}
    id_to_status = {}

    # Find all PLAN files
    plan_files = []
    if vault_path:
        result = subprocess.run(
            ["/usr/bin/find", vault_path, "-name", "PLAN-*.md"],
            capture_output=True,
            text=True,
        )
        plan_files = [l.strip() for l in result.stdout.splitlines() if l.strip()]

    # Parse each plan
    for pf in plan_files:
        data = parse_frontmatter(pf)
        pid = data.get("id") or os.path.basename(pf).replace(".md", "")
        title = data.get("title") or pid
        status = data.get("status") or "unknown"
        parents = data.get("parents") or []
        if isinstance(parents, str):
            parents = [parents]
        id_to_title[pid] = title
        id_to_status[pid] = status
        nodes.append(
            {
                "id": pid,
                "label": title,
                "title": title,
                "status": status,
                "shape": "box",
            }
        )

    # Collect all parent ids that are not already nodes, create placeholder nodes
    parent_ids = set()
    for pf in plan_files:
        data = parse_frontmatter(pf)
        pid = data.get("id") or os.path.basename(pf).replace(".md", "")
        parents = data.get("parents") or []
        if isinstance(parents, str):
            parents = [parents]
        for par in parents:
            parent_ids.add(par)
            # Ensure node exists for parent
            if par not in id_to_title:
                # Create placeholder for feature/parent
                nodes.append(
                    {
                        "id": par,
                        "label": par,
                        "title": par,
                        "status": "parent",
                        "shape": "ellipse",
                    }
                )
                id_to_title[par] = par

    # Build edges
    for pf in plan_files:
        data = parse_frontmatter(pf)
        pid = data.get("id") or os.path.basename(pf).replace(".md", "")
        parents = data.get("parents") or []
        if isinstance(parents, str):
            parents = [parents]
        for par in parents:
            edges.append({"from": par, "to": pid})

    # If no nodes, create a single info node
    if not nodes:
        nodes.append(
            {
                "id": "empty",
                "label": "No plans in vault",
                "title": "No plans",
                "status": "unknown",
                "shape": "box",
            }
        )

    # Load template
    if template_arg and os.path.exists(template_arg):
        template_path = template_arg
    else:
        # Default template
        template_path = "/home/dzack/dotfiles/ags/control-panel/templates/dag.html"
        if not os.path.exists(template_path):
            # Fallback to elegant? But we need dag
            print(f"Template not found: {template_path}", file=sys.stderr)
            sys.exit(1)

    with open(template_path, "r", encoding="utf-8") as f:
        tmpl = f.read()

    # Replace placeholders
    # Use json.dumps for nodes/edges
    nodes_json = json.dumps(nodes, ensure_ascii=False)
    edges_json = json.dumps(edges, ensure_ascii=False)
    # Simple replace
    out_html = (
        tmpl.replace("__VAULT__", vault_name)
        .replace("__REPO__", repo)
        .replace("__NODES_JSON__", nodes_json)
        .replace("__EDGES_JSON__", edges_json)
    )

    # Determine output path
    if not out:
        safe_repo = repo.replace("/", "-")
        out = f"/tmp/{safe_repo}-dag.html"
        if vault_name and vault_name != safe_repo:
            # Use vault name for file
            safe_vault = vault_name.replace("/", "-")
            out = f"/tmp/{safe_vault}-dag.html"

    with open(out, "w", encoding="utf-8") as f:
        f.write(out_html)

    print(out)


if __name__ == "__main__":
    main()
