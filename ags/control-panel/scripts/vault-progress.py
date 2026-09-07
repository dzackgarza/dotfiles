#!/usr/bin/env python3
import json
import os
import re
import subprocess
import sys

vault_base = "/home/dzack/.agent-memory-vault/projects"


def get_progress(repo_short):
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
    if not vault_path or not os.path.isdir(vault_path):
        print(
            json.dumps(
                {
                    "total": 0,
                    "completed": 0,
                    "percent": 0,
                    "vault": "No vault initialized",
                    "activePlan": "No plan active",
                    "activePlanPath": "",
                }
            )
        )
        return
    result = subprocess.run(
        ["/usr/bin/find", vault_path, "-name", "PLAN-*.md"],
        capture_output=True,
        text=True,
    )
    plans = [l.strip() for l in result.stdout.splitlines() if l.strip()]
    total = len(plans)
    completed = 0
    active_candidates = []
    for p in plans:
        try:
            with open(p) as f:
                content = f.read()
                m_status = re.search(r"^status:\s*(.+)", content, re.MULTILINE)
                status = m_status.group(1).strip().strip("\"'") if m_status else ""
                if status == "complete":
                    completed += 1
                if status in [
                    "in-progress",
                    "needs-agent-review",
                    "needs-human-input",
                    "approved-and-unstarted",
                ]:
                    m_title = re.search(r"^title:\s*(.+)", content, re.MULTILINE)
                    title = (
                        m_title.group(1).strip().strip("\"'")
                        if m_title
                        else os.path.basename(p)
                    )
                    mtime = os.path.getmtime(p)
                    active_candidates.append((mtime, status, title, p))
        except:
            pass
    percent = int(completed * 100 / total) if total > 0 else 0
    vault_name = os.path.basename(vault_path)
    activePlan = "No plan active"
    activePlanPath = ""
    if active_candidates:
        active_candidates.sort(key=lambda x: x[0], reverse=True)
        activePlan = active_candidates[0][2]
        activePlanPath = active_candidates[0][3]
    print(
        json.dumps(
            {
                "total": total,
                "completed": completed,
                "percent": percent,
                "vault": vault_name,
                "activePlan": activePlan,
                "activePlanPath": activePlanPath,
            }
        )
    )


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(
            json.dumps(
                {
                    "total": 0,
                    "completed": 0,
                    "percent": 0,
                    "vault": "No vault initialized",
                    "activePlan": "No plan active",
                    "activePlanPath": "",
                }
            )
        )
    else:
        get_progress(sys.argv[1])
