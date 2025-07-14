#!/usr/bin/env python3

import json
import subprocess
import tempfile
from pathlib import Path

git_root = Path(subprocess.run(["git", "rev-parse", "--show-toplevel"], capture_output=True, text=True, check=True).stdout.strip())
writing_dir = git_root / "writing"
md_files = list(writing_dir.rglob("*.md"))

combined_md = []
for md_file in md_files:
    combined_md.append(md_file.read_text())
    combined_md.append("\n\n")

with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False) as temp_md:
    temp_md.write("\n".join(combined_md))
    temp_md_path = temp_md.name

try:
    result = subprocess.run(["pandoc", temp_md_path, "-t", "json"], capture_output=True, text=True, check=True, stderr=subprocess.DEVNULL)
    ast_data = json.loads(result.stdout)
finally:
    Path(temp_md_path).unlink()

div_ids = set()

def walk_ast(element):
    if isinstance(element, dict):
        if element.get("t") == "Div":
            attrs = element.get("c", [])
            if len(attrs) >= 2 and len(attrs[0]) >= 2:
                div_id, classes = attrs[0][0], attrs[0][1]
                if div_id and classes:
                    div_ids.add(div_id)
        for value in element.values():
            if isinstance(value, (dict, list)):
                walk_ast(value)
    elif isinstance(element, list):
        for item in element:
            if isinstance(item, (dict, list)):
                walk_ast(item)

walk_ast(ast_data)

for div_id in sorted(div_ids):
    print(f"#{div_id}")
