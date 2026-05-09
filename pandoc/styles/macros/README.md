# LaTeX Macro Library Organization

**Location:** `~/.pandoc/core/lib/`

This directory contains the organized LaTeX macro library, consolidated from scattered legacy files into a tier-based system.

## Tier System

### Tier 1: Simple MathJax-Compatible Shortcuts
**File:** `tier1-mathjax-simple.tex`

**Criteria:**
- `\newcommand` or `\DeclareMathOperator` with NO arguments
- Only uses MathJax-safe primitives: `\mathbb`, `\mathcal`, `\mathsf`, `\mathrm`, `\mathfrak`
- No `\makeatletter`, `\mathpalette`, or TeX programming constructs

**Examples:**
```latex
\newcommand{\ZZ}{\mathbb{Z}}
\newcommand{\QQ}{\mathbb{Q}}
\newcommand{\RR}{\mathbb{R}}
\newcommand{\CC}{\mathbb{C}}
\DeclareMathOperator{\Hom}{Hom}
\DeclareMathOperator{\Aut}{Aut}
```

**Works in:** LaTeX, Pandoc, Obsidian MathJax

### Tier 2: Commands with Arguments (MathJax-Compatible)
**File:** `tier2-mathjax-args.tex`

**Criteria:**
- `\newcommand` with 1-9 arguments
- Uses only MathJax-safe constructs: `\left`, `\right`, `\frac`, `\text`, basic math mode
- No spacing hacks (`\,`, `\!`, `\mkern`), no boxes, no `\mathchoice`

**Examples:**
```latex
\newcommand{\gens}[1]{\left\langle{#1}\right\rangle}
\newcommand{\abs}[1]{{\left\lvert #1 \right\rvert}}
\newcommand{\norm}[1]{{\left\lVert #1 \right\rVert}}
\newcommand{\dd}[2]{\frac{\partial #1}{\partial #2}}
```

**Works in:** LaTeX, Pandoc, Obsidian MathJax

### Tier 3: Complex TeX-Specific Commands
**File:** `tier3-tex-complex.tex`

**Criteria:**
- Uses TeX primitives not in MathJax: `\mathpalette`, `\ooalign`, `\mathchoice`
- Spacing/kerning hacks: `\mkern`, `\mskip`, `\phantom`
- Box manipulation: `\hbox`, `\vbox`, `\rlap`, `\llap`
- `\makeatletter` ... `\makeatother` blocks

**Examples:**
```latex
\makeatletter
\newcommand{\superimpose}[2]{%
  {\ooalign{$#1$\cr\hfil$#2$\hfil\cr}}%
}
\makeatother
```

**Works in:** LaTeX, Pandoc only (NOT Obsidian MathJax)

### Tier 4: Preamble Content (Package Loading & Document Setup)
**File:** `tier4-preamble.tex`

**Criteria:**
- `\usepackage` statements
- `\setkomafont`, `\addtokomafont`, page geometry
- `\hypersetup`, `\definecolor`, global theorem styles
- Anything that configures document-level behavior

**Examples:**
```latex
\usepackage{amsmath,amsthm,amssymb}
\usepackage{tikz-cd}
\usetikzlibrary{arrows,positioning}
\hypersetup{colorlinks=true, linkcolor=blue}
```

**Works in:** LaTeX, Pandoc only (document-level configuration)

## Domain-Specific Files

**`categories.tex`:**
- Category theory macros (from `latexmacs_categories.tex`)
- Organized internally by tier (tier 1 shortcuts, tier 2 commands, tier 3 complex)
- Clear section headers for each tier

**`spectral.tex`:**
- Spectral sequence macros (from `latexmacs_spectra.tex`)
- Same internal tier organization

**`tikz.tex`:**
- Consolidated TikZ styles, node definitions, edge styles
- Merged from `tikz_macros.tex` + `tikzmacros.tex` + `Tikz_Macros.tex`
- Inherently tier 3 (LaTeX-only)

**`environments.tex`:**
- Preserved from `macros/environments.tex`
- Theorem environment styling with tcolorbox
- Tier 4 content (document-level setup)

## Adding New Macros

### Decision Tree

```
Does it load packages or configure document? → Tier 4 (tier4-preamble.tex)
Does it use TeX primitives (\mathpalette, boxes)? → Tier 3 (tier3-tex-complex.tex)
Does it take arguments? → Tier 2 (tier2-mathjax-args.tex)
Is it a simple shortcut? → Tier 1 (tier1-mathjax-simple.tex)
Is it domain-specific? → categories.tex, spectral.tex, or tikz.tex
```

### Organization Guidelines

1. **Determine tier** using decision tree above
2. **Add to appropriate file:**
   - General macros: tier1/tier2/tier3/tier4 files
   - Category theory: `categories.tex`
   - Spectral sequences: `spectral.tex`
   - TikZ content: `tikz.tex`
3. **Organize within file:**
   - Alphabetical by command name, OR
   - Grouped by topic with clear section comments
4. **MathJax compatibility:**
   - If Obsidian-safe (tiers 1-2), it auto-loads in Obsidian on reload
   - Tiers 3-4 are LaTeX/Pandoc only

## Migration History

**Migrated from** `macros/` directory on 2025-01-09

**Source files consolidated:**
- `latexmacs.tex` (980 lines) → tier files
- `latexmacs_categories.tex` (267 lines) → `categories.tex`
- `latexmacs_spectra.tex` (41 lines) → `spectral.tex`
- `latexmacs_commands.tex` (150 lines) → tier files
- `tikz_macros.tex` + `tikzmacros.tex` → `tikz.tex`
- `environments.tex` → `environments.tex` (preserved as-is)

**Legacy files archived to:** `archive/legacy-macros-2025-01-09/`

## Usage

### In LaTeX/Pandoc Documents

Load all macros via unified style:
```latex
\usepackage{dzg-unified}
```

### In Obsidian

MathJax-safe subset (tiers 1+2 only) loads automatically via symlinked `mathjax-macros.tex` in `.obsidian/` directory.

See `obsidian/README.md` for setup instructions.
