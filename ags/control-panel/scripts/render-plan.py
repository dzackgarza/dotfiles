#!/usr/bin/env python3
import os
import subprocess
import sys
import tempfile


def extract_yaml_raw(plan_path):
    try:
        with open(plan_path, "r", encoding="utf-8") as f:
            content = f.read()
        lines = content.splitlines()
        if len(lines) >= 2 and lines[0].strip() == "---":
            for i in range(1, len(lines)):
                if lines[i].strip() == "---":
                    raw = "\n".join(lines[1:i])
                    return raw
        return ""
    except Exception:
        return ""


def main():
    if len(sys.argv) < 3:
        print(
            f"Usage: {sys.argv[0]} <planPath> <repo> [vault] [template] [out]",
            file=sys.stderr,
        )
        sys.exit(1)
    plan_path = sys.argv[1]
    repo = sys.argv[2] if len(sys.argv) > 2 else ""
    vault = ""
    template = ""
    out = "/tmp/plan.html"
    # Flexible arg handling
    if len(sys.argv) == 4:
        # planPath, repo, template
        template = sys.argv[3]
    elif len(sys.argv) == 5:
        # Could be planPath, repo, template, out OR planPath, repo, vault, template
        if sys.argv[3].endswith(".html") or ".template" in sys.argv[3]:
            template = sys.argv[3]
            out = sys.argv[4]
        else:
            vault = sys.argv[3]
            template = sys.argv[4]
    elif len(sys.argv) >= 6:
        vault = sys.argv[3] if len(sys.argv) > 3 else ""
        template = sys.argv[4] if len(sys.argv) > 4 else ""
        out = sys.argv[5] if len(sys.argv) > 5 else "/tmp/plan.html"
    # Derive vault from plan_path if not given
    if not vault and plan_path:
        parts = plan_path.split("/")
        if "projects" in parts:
            idx = parts.index("projects")
            if idx + 1 < len(parts):
                vault = parts[idx + 1]
    raw_yaml = extract_yaml_raw(plan_path)
    meta_fd, meta_path = tempfile.mkstemp(suffix=".yaml", prefix="plan-meta-")
    try:
        with os.fdopen(meta_fd, "w", encoding="utf-8") as mf:
            mf.write("---\n")
            if raw_yaml:
                mf.write("yaml_raw: |\n")
                for line in raw_yaml.splitlines():
                    mf.write(f"  {line}\n")
            if repo:
                repo_esc = repo.replace('"', '\\"')
                mf.write(f'repo: "{repo_esc}"\n')
            if vault:
                vault_esc = vault.replace('"', '\\"')
                mf.write(f'vault: "{vault_esc}"\n')
            mf.write("...\n")
        args = ["pandoc", plan_path, "--metadata-file", meta_path, "-s", "-o", out]
        if template and os.path.exists(template):
            args.extend(["--template", template])
        result = subprocess.run(args, capture_output=True, text=True)
        if result.returncode != 0:
            print(f"pandoc failed: {result.stderr}", file=sys.stderr)
            sys.exit(result.returncode)
        # Post-process to fix raw YAML display: pandoc wraps yaml_raw as <p> inside <pre><code>
        # Replace with correctly escaped raw YAML
        if raw_yaml and os.path.exists(out):
            try:
                import html
                import re
                with open(out, 'r', encoding='utf-8') as f:
                    html_content = f.read()
                escaped = html.escape(raw_yaml)
                # Replace the inner of <pre class="yaml-raw"><code>...</code></pre>
                # The pandoc output currently has <pre class="yaml-raw"><code><p>...</p></code></pre> or similar
                pattern = r'<pre class="yaml-raw"><code>.*?</code></pre>'
                replacement = f'<pre class="yaml-raw"><code>{escaped}</code></pre>'
                new_html, n = re.subn(pattern, replacement, html_content, flags=re.DOTALL)
                if n == 0:
                    # Fallback: try without class
                    pattern2 = r'<pre><code>.*?</code></pre>'
                    # Only replace if yaml_raw is inside
                    pass
                else:
                    with open(out, 'w', encoding='utf-8') as f:
                        f.write(new_html)
            except Exception as e:
                print(f"post-process failed: {e}", file=sys.stderr)
        print(f"Rendered {plan_path} -> {out}")
    finally:
        try:
            os.remove(meta_path)
        except:
            pass


if __name__ == "__main__":
    main()
