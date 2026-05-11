import os
import subprocess
import tempfile
import pathlib

ROOT = pathlib.Path(__file__).parent.parent

TEMPLATE = r"""
\documentclass[tikz, border=2pt]{{standalone}}
\usepackage{{dzg-unified}}
\usepackage{{tikzit}}
\usepackage{{dynkin-diagrams}}
\usepackage{{quiver}}

\usetikzlibrary{{
    arrows.meta, cd, fadings, patterns, calc, matrix, 
    positioning, decorations, decorations.pathreplacing, 
    decorations.markings, shapes, backgrounds, fit, 
    shapes.geometric, intersections, hobby,
    arrows, decorations.pathmorphing
}}

\begin{{document}}
{content}
\end{{document}}
"""

def render_tikz(filepath: str, output_dir: str) -> bool:
    with open(filepath, 'r') as f:
        content = f.read()

    # Determine if it's tikz or tikzcd
    if 'tikzcd' in filepath:
        # Wrap in shorthand or ensure environment is correct
        pass

    tex_content = TEMPLATE.format(content=content)
    
    name = pathlib.Path(filepath).stem
    with tempfile.TemporaryDirectory() as tmpdir:
        tex_file = os.path.join(tmpdir, f"{name}.tex")
        with open(tex_file, 'w') as f:
            f.write(tex_content)
        
        # Do not override TEXINPUTS, rely on global environment from .zshrc/.envrc
        
        # Compile to PDF
        try:
            # Use -interaction=nonstopmode for speed
            subprocess.run(
                ["pdflatex", "-interaction=nonstopmode", tex_file],
                cwd=tmpdir, check=True, capture_output=True, text=True
            )
        except subprocess.CalledProcessError as e:
            pdf_file = os.path.join(tmpdir, f"{name}.pdf")
            if os.path.exists(pdf_file):
                print(f"Warnings during compilation of {filepath}, but PDF produced.")
            else:
                print(f"Error compiling {filepath}:")
                print(e.stdout)
                print(e.stderr)
                return False

        pdf_file = os.path.join(tmpdir, f"{name}.pdf")
        svg_file = os.path.join(output_dir, f"{name}.svg")
        target_pdf_file = os.path.join(output_dir, f"{name}.pdf")
        
        # Convert to SVG
        try:
            subprocess.run(["pdf2svg", pdf_file, svg_file], check=True)
            # Use shutil to copy the pdf
            import shutil
            shutil.copy(pdf_file, target_pdf_file)
        except subprocess.CalledProcessError as e:
            print(f"Error converting {pdf_file} to SVG or copying PDF:")
            return False
            
    print(f"Rendered {name}.svg")
    return True

def main():
    tikz_dirs = [
        pathlib.Path("/home/dzack/figures/tikz"),
        pathlib.Path("/home/dzack/figures/tikzcd")
    ]
    output_dir = pathlib.Path("/home/dzack/figures/rendered")
    output_dir.mkdir(parents=True, exist_ok=True)

    for tikz_dir in tikz_dirs:
        if not tikz_dir.exists():
            print(f"Directory {tikz_dir} does not exist. Skipping.")
            continue
        for tex_file in tikz_dir.glob("*.tex"):
            render_tikz(str(tex_file), str(output_dir))

if __name__ == "__main__":
    main()
