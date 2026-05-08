#!/usr/bin/env python3
import re
import argparse
import subprocess
import tempfile
from pathlib import Path

def parse_macros(sty_file):
    r"""
    Parses LaTeX macros from a .sty file.
    Supports \newcommand, \providecommand, \renewcommand, and \DeclareMathOperator.
    Handles 0, 1, and 2 arguments.
    """
    if not sty_file or not Path(sty_file).exists():
        return {}, {}, {}

    with open(sty_file, 'r') as f:
        sty_content = f.read()

    # Remove all comments
    sty_content = re.sub(r'(?m)%.*$', '', sty_content)
    
    macros_0 = {}
    macros_1 = {}
    macros_2 = {}
    
    idx = 0
    while True:
        # Match \newcommand, \providecommand, \renewcommand, or \DeclareMathOperator
        match = re.search(r'\\(newcommand|providecommand|renewcommand|DeclareMathOperator)\*?\s*\{\s*\\([a-zA-Z]+)\s*\}', sty_content[idx:])
        if not match:
            break
            
        cmd_type = match.group(1)
        name = match.group(2)
        start = idx + match.end()
        idx = start
        
        # Check args
        args_count = 0
        if idx < len(sty_content) and sty_content[idx] == '[':
            # find matching bracket
            b_end = sty_content.find(']', idx)
            if b_end != -1:
                try:
                    args_count = int(sty_content[idx+1:b_end])
                except:
                    pass
                idx = b_end + 1
                
        # skip space
        while idx < len(sty_content) and sty_content[idx] in ' \n\t\r':
            idx += 1
            
        if idx < len(sty_content) and sty_content[idx] == '{':
            depth = 1
            brace_start = idx
            idx += 1
            while idx < len(sty_content) and depth > 0:
                if sty_content[idx] == '{': depth += 1
                elif sty_content[idx] == '}': depth -= 1
                elif sty_content[idx] == '\\': 
                    idx += 1 # skip escaped braces
                idx += 1
                
            if depth == 0:
                body = sty_content[brace_start+1:idx-1]
                if cmd_type == 'DeclareMathOperator':
                    macros_0[name] = r"\operatorname{" + body + "}"
                else:
                    if args_count == 0:
                        macros_0[name] = body
                    elif args_count == 1:
                        macros_1[name] = body
                    elif args_count == 2:
                        macros_2[name] = body
                        
    return macros_0, macros_1, macros_2

def expand_macros(text, macros_0, macros_1, macros_2, max_passes=5):
    r"""
    Expands LaTeX macros in the given text.
    """
    changed = True
    macro_names = sorted(list(macros_0.keys()) + list(macros_1.keys()) + list(macros_2.keys()), key=len, reverse=True)
    
    passes = 0
    while changed and passes < max_passes:
        changed = False
        passes += 1
        
        for name in macro_names:
            idx = 0
            # compile regex for faster search
            pattern = re.compile(r'\\' + re.escape(name) + r'(?![a-zA-Z])')
            while True:
                match = pattern.search(text, idx)
                if not match:
                    break
                    
                start = match.start()
                end = match.end()
                
                if name in macros_0:
                    body = macros_0[name]
                    text = text[:start] + body + text[end:]
                    changed = True
                    idx = start + len(body)
                    continue
                    
                args_needed = 1 if name in macros_1 else 2
                args = []
                curr_idx = end
                
                valid = True
                for _ in range(args_needed):
                    while curr_idx < len(text) and text[curr_idx] in ' \n\t\r':
                        curr_idx += 1
                        
                    if curr_idx < len(text) and text[curr_idx] == '{':
                        brace_start = curr_idx
                        depth = 1
                        curr_idx += 1
                        while curr_idx < len(text) and depth > 0:
                            if text[curr_idx] == '{': depth += 1
                            elif text[curr_idx] == '}': depth -= 1
                            elif text[curr_idx] == '\\': curr_idx += 1
                            curr_idx += 1
                            
                        if depth == 0:
                            args.append(text[brace_start+1:curr_idx-1])
                        else:
                            valid = False
                            break
                    else:
                        if curr_idx < len(text):
                            if text[curr_idx] == '\\':
                                # consume the entire macro as one token
                                m = re.match(r'\\[a-zA-Z]+', text[curr_idx:])
                                if m:
                                    args.append(m.group(0))
                                    curr_idx += m.end()
                                else:
                                    args.append(text[curr_idx])
                                    curr_idx += 1
                            else:
                                args.append(text[curr_idx])
                                curr_idx += 1
                        else:
                            valid = False
                            break
                            
                if valid:
                    if name in macros_1:
                        body = macros_1[name].replace('#1', args[0])
                    else:
                        body = macros_2[name].replace('#1', args[0]).replace('#2', args[1])
                    text = text[:start] + body + text[curr_idx:]
                    changed = True
                    idx = start + len(body)
                else:
                    idx = end
                    
    return text

def strip_tex_formatting(text):
    r"""
    Strips Pandoc/LaTeX artifacts from the expanded text.
    """
    # Pandoc outputs raw tex wrappers like `\mathrm{II}`{=tex} in markdown+raw_tex
    text = re.sub(r'`(.*?)`\{=tex\}', r'\1', text)
    # Strip display math blocks if they appeared
    text = re.sub(r'```tex\n(.*?)\n```', r'\1', text, flags=re.DOTALL)
    # Restore escaped brackets
    text = text.replace(r'\[', '[').replace(r'\]', ']')
    return text


def preprocess_citations(text):
    r"""
    Converts LaTeX \cite{...} followed by suffixes to Pandoc-style [@...] citations.
    Also fixes MathJax-style \( \) math syntax.
    """
    def cite_replacer(match):
        suffix = match.group(1)
        keys_str = match.group(2)
        keys = [k.strip() for k in keys_str.split(',')]
        formatted_keys = []
        for i, k in enumerate(keys):
            if i == len(keys) - 1 and suffix:
                formatted_keys.append(f"@{k}, {suffix}")
            else:
                formatted_keys.append(f"@{k}")
        return "[" + "; ".join(formatted_keys) + "]"
        
    text = re.sub(r'\\cite\[(.*?)\]\{(.*?)\}', cite_replacer, text)
    text = re.sub(r'\\cite\{(.*?)\}', lambda m: "[" + "; ".join(f"@{k.strip()}" for k in m.group(1).split(',')) + "]", text)
    
    # Fix MathJax-style \( \) inline math syntax so Pandoc parses it as math
    text = text.replace(r'\(', '$').replace(r'\)', '$')
    return text

def resolve_citations(text, bib_file):
    r"""
    Uses Pandoc to resolve citations in the given text using the provided bibliography.
    """
    if not bib_file or not Path(bib_file).exists():
        print(f"Warning: Bibliography file {bib_file} not found. Skipping citation resolution.")
        return text

    with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False) as tmp_in:
        tmp_in.write(text)
        tmp_in_path = tmp_in.name

    tmp_out_path = tmp_in_path + ".out.md"
    
    try:
        subprocess.run([
            "pandoc",
            "--from=markdown",
            "--to=markdown-citations+tex_math_dollars+raw_tex",
            "--citeproc",
            f"--bibliography={bib_file}",
            "--standalone",
            "--wrap=none",
            tmp_in_path,
            "-o", tmp_out_path
        ], check=True)
        
        with open(tmp_out_path, 'r') as f:
            result = f.read()
        return result
    finally:
        Path(tmp_in_path).unlink(missing_ok=True)
        Path(tmp_out_path).unlink(missing_ok=True)

def expand_all(text, sty_file=None, bib_file=None, strip=True):
    r"""
    Orchestrates the full expansion process: citations -> macros -> cleanup.
    """
    print("Pre-processing citations...")
    text = preprocess_citations(text)
    
    if bib_file:
        print("Resolving citations...")
        text = resolve_citations(text, bib_file)
        
    if sty_file:
        print("Parsing and expanding macros...")
        m0, m1, m2 = parse_macros(sty_file)
        print(f"Loaded {len(m0)} 0-arg, {len(m1)} 1-arg, {len(m2)} 2-arg macros.")
        text = expand_macros(text, m0, m1, m2)
        
    if strip:
        print("Cleaning up formatting...")
        text = strip_tex_formatting(text)
        
    return text

def main():
    parser = argparse.ArgumentParser(description="Expand LaTeX macros and citations in a file.")
    parser.add_argument("input", help="Input file (Markdown/LaTeX)")
    parser.add_argument("--sty", help="LaTeX style file (.sty) containing macro definitions")
    parser.add_argument("--bib", help="Bibliography file (.bib) for citation resolution")
    parser.add_argument("--output", help="Output file")
    parser.add_argument("--no-strip", action="store_false", dest="strip", help="Do not strip LaTeX/Pandoc artifacts")
    parser.get_default("strip") # ensure strip defaults to True if omit --no-strip
    
    args = parser.parse_args()
    strip = getattr(args, 'strip', True)
    
    with open(args.input, 'r') as f:
        text = f.read()
        
    text = expand_all(text, sty_file=args.sty, bib_file=args.bib, strip=strip)
        
    if args.output:
        with open(args.output, 'w') as f:
            f.write(text)
        print(f"Expanded output written to {args.output}")
    else:
        print(text)

if __name__ == "__main__":
    main()
