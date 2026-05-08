# Pandoc Configuration & LaTeX Macro Library

Personal Pandoc configuration and LaTeX macro library, organized for use with both Pandoc and pure LaTeX documents.

## Directory Structure

```
pandoc/
├── core/                    # Core LaTeX macro system
│   ├── lib/                # Organized macro library (tier system)
│   ├── styles/             # .sty packages (dzg-unified, dzg-mathjax, external deps)
│   ├── preambles/          # Modern document preambles (KOMA, AMS)
│   └── obsidian/           # MathJax subset for Obsidian
├── templates/              # Pandoc and LaTeX templates
├── filters/                # Pandoc Lua filters
├── config/                 # Miscellaneous configuration
├── bin/                    # Build scripts and utilities
├── tests/                  # Test suite for macro system
└── archive/                # Archived legacy files
```

## Quick Start

### For LaTeX Documents

```latex
\documentclass{article}
\usepackage{dzg-unified}  % Loads all tiers and domain files
\begin{document}
$\ZZ, \QQ, \RR, \CC$
\end{document}
```

### With Modern Preambles

```latex
\input{koma-article}  % Automatically includes dzg-unified
\begin{document}
% All macros available
\end{document}
```

### For Obsidian

1. Symlink the MathJax macros:
```bash
ln -s ~/dotfiles/pandoc/core/obsidian/mathjax-macros.tex \
      ~/notes/Obsidian/.obsidian/mathjax-macros.tex
```

2. Configure better-mathjax plugin to load `.obsidian/mathjax-macros.tex`

3. Tiers 1-2 macros work in math blocks

## Environment Setup

Add to `~/.zshrc`:

```bash
export TEXINPUTS=".:$HOME/figures//:$HOME/.pandoc/core/styles//:$HOME/.pandoc/core/lib//:$HOME/.pandoc/core/preambles//:$HOME/.pandoc/config//:"
export BIBINPUTS=".:$HOME/.pandoc/bib//:${BIBINPUTS:-}"
export PATH="$HOME/.pandoc/bin:$PATH"
```

Reload: `source ~/.zshrc`

## Macro Tier System

The macro library in `core/lib/` is organized into 4 tiers based on MathJax compatibility:

- **Tier 1**: Simple shortcuts (MathJax-safe, no arguments)
- **Tier 2**: Commands with arguments (MathJax-safe)
- **Tier 3**: Complex TeX (LaTeX-only)
- **Tier 4**: Package-dependent declarations (LaTeX-only)

Plus domain-specific files: categories.tex, spectral.tex, tikz.tex, environments.tex

See `core/lib/README.md` for detailed tier guidelines.

## Style Packages

- **dzg-unified.sty**: Main package, loads all tiers (for LaTeX/Pandoc)
- **dzg-mathjax.sty**: MathJax subset (tiers 1-2 only, for Obsidian)
- External dependencies: freetikz.sty, quiver.sty, tikzit.sty

## Documentation

- `MIGRATION-COMPLETE.md`: Full migration history and statistics
- `core/lib/README.md`: Tier system guidelines and decision tree
- `core/preambles/README.md`: Preamble usage guide
- `core/obsidian/README.md`: Obsidian setup instructions
- `tests/README.md`: Test suite documentation

## Statistics

- **Total macros**: 2,318 lines organized from 2,926 scattered lines
- **MathJax-compatible**: 1,257 macros (tiers 1-2) work in Obsidian
- **Test coverage**: 100+ different macro types verified
- **Templates**: 6 templates migrated to unified system

## Related Projects

- **Dissertation**: More comprehensive `DZG-Macros.sty` (1,664 lines) at `~/diss` includes dissertation-specific packages (minted, algorithm2e, dynkin-diagrams)
- This library is the canonical general-purpose macro system
