#!/usr/bin/env python3
import os
import subprocess
import sys
import tempfile


def extract_yaml_raw(plan_path):
    try:
        with open(plan_path, "r", encoding="utf-8") as f:
            content = f.read()
        # Find first --- and second ---
        lines = content.splitlines()
        if len(lines) >= 2 and lines[0].strip() == "---":
            # find second ---
            for i in range(1, len(lines)):
                if lines[i].strip() == "---":
                    raw = "\n".join(lines[1:i])
                    return raw
        return ""
    except Exception:
        return ""


def main():
    if len(sys.argv) < 5:
        print(
            f"Usage: {sys.argv[0]} <planPath> <repo> <vault> <template> <out>",
            file=sys.stderr,
        )
        sys.exit(1)
    plan_path = sys.argv[1]
    repo = sys.argv[2] if len(sys.argv) > 2 else ""
    vault = sys.argv[3] if len(sys.argv) > 3 else ""
    template = sys.argv[4] if len(sys.argv) > 4 else ""
    out = sys.argv[5] if len(sys.argv) > 5 else "/tmp/plan.html"

    raw_yaml = extract_yaml_raw(plan_path)
    # Create temp metadata file
    # Use yaml_raw as literal block scalar
    meta_fd, meta_path = tempfile.mkstemp(suffix=".yaml", prefix="plan-meta-")
    try:
        with os.fdopen(meta_fd, "w", encoding="utf-8") as mf:
            mf.write("---\n")
            if raw_yaml:
                mf.write("yaml_raw: |\n")
                for line in raw_yaml.splitlines():
                    mf.write(f"  {line}\n")
            if repo:
                # escape repo
                repo_esc = repo.replace('"', '\\"')
                mf.write(f'repo: "{repo_esc}"\n')
            if vault:
                vault_esc = vault.replace('"', '\\"')
                mf.write(f'vault: "{vault_esc}"\n')
            mf.write("...\n")
        # Build pandoc args
        args = ["pandoc", plan_path, "--metadata-file", meta_path, "-s", "-o", out]
        if template and os.path.exists(template):
            args.extend(["--template", template])
        # Add highlighting
        # pandoc will auto use highlighting-css if template has $highlighting-css$
        result = subprocess.run(args, capture_output=True, text=True)
        if result.returncode != 0:
            print(f"pandoc failed: {result.stderr}", file=sys.stderr)
            sys.exit(result.returncode)
        print(f"Rendered {plan_path} -> {out}")
    finally:
        try:
            os.remove(meta_path)
        except:
            pass


if __name__ == "__main__":
    main()
