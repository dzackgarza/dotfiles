import json
import sys
import os
from pygments import highlight
from pygments.lexers import PythonLexer, MarkdownLexer
from pygments.formatters import Terminal256Formatter

def render_ipynb(filepath, start_line=1, end_line=1000):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            nb = json.load(f)
    except Exception as e:
        print(f"Failed to parse notebook: {e}")
        return

    py_lexer = PythonLexer()
    md_lexer = MarkdownLexer()
    formatter = Terminal256Formatter(style='monokai')

    lines = []

    cells = nb.get('cells', [])
    for i, cell in enumerate(cells):
        cell_type = cell.get('cell_type', '')
        source = ''.join(cell.get('source', []))
        
        if cell_type == 'markdown':
            header = f"\033[1;34m--- [Markdown Cell {i+1}] ---\033[0m"
            lines.append(header)
            if source.strip():
                rendered = highlight(source, md_lexer, formatter).rstrip()
                lines.extend(rendered.splitlines())
            lines.append("")

        elif cell_type == 'code':
            exec_count = cell.get('execution_count')
            cnt_str = f"[{exec_count}]" if exec_count is not None else "[ ]"
            header = f"\033[1;32mIn {cnt_str}:\033[0m"
            lines.append(header)
            if source.strip():
                rendered = highlight(source, py_lexer, formatter).rstrip()
                lines.extend(rendered.splitlines())
            
            outputs = cell.get('outputs', [])
            for out in outputs:
                out_type = out.get('output_type', '')
                if out_type == 'stream':
                    out_hdr = f"\033[1;33mOut {cnt_str}:\033[0m"
                    lines.append(out_hdr)
                    lines.extend(''.join(out.get('text', [])).rstrip().splitlines())
                elif out_type in ('execute_result', 'display_data'):
                    data = out.get('data', {})
                    if 'text/plain' in data:
                        out_hdr = f"\033[1;33mOut {cnt_str}:\033[0m"
                        lines.append(out_hdr)
                        lines.extend(''.join(data['text/plain']).rstrip().splitlines())
                elif out_type == 'error':
                    out_hdr = f"\033[1;31mOut {cnt_str} (Error):\033[0m"
                    lines.append(out_hdr)
                    lines.extend('\n'.join(out.get('traceback', [])).rstrip().splitlines())
            lines.append("")

    sliced = lines[max(0, start_line - 1) : end_line]
    print("\n".join(sliced))

if __name__ == '__main__':
    if len(sys.argv) >= 2:
        fp = sys.argv[1]
        s = int(sys.argv[2]) if len(sys.argv) >= 3 else 1
        e = int(sys.argv[3]) if len(sys.argv) >= 4 else 1000
        render_ipynb(fp, s, e)
