# Pandoc Configuration

Personal Pandoc and LaTeX configuration for generating PDFs from markdown and managing LaTeX macros.

## Directory Structure

```
styles/                     # LaTeX macro system (styles assemble macros)
├── dzg-unified.sty        # Main style - loads all macros
├── dzg-mathjax.sty        # MathJax subset (tiers 1-2)
├── freetikz.sty           # External TikZ helper
├── quiver.sty             # Commutative diagrams
├── tikzit.sty             # TikZ editor integration
├── macros/                # Raw .tex macro files (tier system)
│   ├── tier1-mathjax-simple.tex
│   ├── tier2-mathjax-args.tex
│   ├── tier3-tex-complex.tex
│   ├── tier4-preamble.tex
│   ├── categories.tex
│   ├── spectral.tex
│   ├── tikz.tex
│   └── environments.tex
├── preambles/             # Document preambles
│   ├── koma-article.tex
│   └── ams-article.tex
└── obsidian/              # MathJax macros for Obsidian
    └── mathjax-macros.tex

templates/                  # Pandoc and LaTeX templates
├── *.tex, *.html, *.latex
├── css/                   # CSS for HTML templates
└── metadata/              # YAML metadata files

bin/                        # Scripts and Lua filters
├── *.lua                  # Pandoc Lua filters
├── *.sh                   # Shell scripts
└── *.py                   # Python utilities

config/                     # Miscellaneous configuration
tests/                      # Test suite
bib/                        # Bibliography files
archive/                    # Archived legacy files
```

## Usage

### LaTeX Documents

```latex
\documentclass{article}
\usepackage{dzg-unified}  % Loads all macros
\begin{document}
$\ZZ, \QQ, \RR, \CC$
\end{document}
```

### Pandoc

```bash
pandoc input.md -o output.pdf \
    --template=pandoc_template.tex \
    -H styles/dzg-unified.sty
```

### Environment Setup

Required in `~/.zshrc`:

```bash
export TEXINPUTS=".:$HOME/figures//:$HOME/.pandoc/styles//:$HOME/.pandoc/styles/macros//:$HOME/.pandoc/styles/preambles//:$HOME/.pandoc/config//:"
export BIBINPUTS=".:$HOME/.pandoc/bib//:${BIBINPUTS:-}"
export PATH="$HOME/.pandoc/bin:$PATH"
```

## Macro Tier System

Macros in `styles/macros/` organized by MathJax compatibility:

- **Tier 1**: Simple shortcuts, no args (MathJax-safe)
- **Tier 2**: With arguments (MathJax-safe)
- **Tier 3**: Complex TeX primitives (LaTeX-only)
- **Tier 4**: Package-dependent (LaTeX-only)

Plus domain files: categories, spectral, tikz, environments.

## Key Files

- **dzg-unified.sty**: Main unified package (loads all tiers)
- **dzg-mathjax.sty**: MathJax subset for Obsidian (tiers 1-2 only)
- **preambles/**: Modern document preambles (KOMA-Script, AMS)
- **bin/*.lua**: Pandoc filters (tikzcd, callouts, image handling)
- **tests/**: Comprehensive test suite verifying all macros compile

See subdirectory READMEs for detailed documentation.
