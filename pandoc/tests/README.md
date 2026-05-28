# LaTeX Macro System - Test Documents

This directory contains test documents that exercise the unified LaTeX macro system.

## Test Files

### LaTeX Test

- **test-latex-macros.tex** - Comprehensive LaTeX document testing all macro tiers
- **test-latex-macros.pdf** - Compiled output (206KB, 4 pages)
- **test-macros.sty** - Test-specific package with absolute paths to lib/

### Pandoc Test

- **test-pandoc-macros.md** - Markdown document with same macro tests
- **compile-pandoc-test.sh** - Compilation script (work in progress)

## Compiling the LaTeX Test

The LaTeX test compiles successfully:

```bash
cd /home/dzack/dotfiles/pandoc/tests
pdflatex -interaction=nonstopmode test-latex-macros.tex
```

This produces `test-latex-macros.pdf` which exercises:
- **Tier 1:** Number systems (ℤ, ℚ, ℝ, ℂ), operators (Hom, Aut, Ext, Tor)
- **Tier 2:** Delimiters (abs, norm, gens), constructions (fps, laurent)
- **Tier 3:** Matrices (matt, cvec), stacking (stack)
- **Tier 4:** Declared operators (spanof, supp, hilb)
- **Categories:** Category names (Set, Grp, Ring), limits/colimits
- **Spectral:** Bordism spectra (MO, MSO), K-theory (KO, KU), tmf

## Known Issues

### Command Conflicts

Some macros conflict with LaTeX defaults:
- `\ae` (already defined by LaTeX)
- `\mod`, `\qed`, `\too` (conflicts with standard commands)

These are handled by the macro files but may generate warnings.

### TEXINPUTS Configuration

For the macro system to work correctly in production, TEXINPUTS must include:
```bash
export TEXINPUTS=".:$HOME/.pandoc/styles//:$HOME/.pandoc/lib//:$HOME/.pandoc/preambles//:$HOME/.pandoc/config//:"
```

This is already configured in `~/.zshrc`. Reload your shell or run `source ~/.zshrc` to
apply.

### Test-Specific Package

`test-macros.sty` uses absolute paths to avoid TEXINPUTS issues during testing.
In production, use `\usepackage{dzg-unified}` instead (requires TEXINPUTS).

## What the Tests Verify

✅ **Tier 1 macros** (simple shortcuts) compile without errors ✅ **Tier 2 macros** (with
arguments) render correctly ✅ **Tier 3 macros** (complex TeX) produce correct output ✅
**Tier 4 macros** (DeclareMathOperator) work with amsmath loaded ✅ **Category theory
macros** from categories.tex work ✅ **Spectral sequence macros** from spectral.tex work
✅ **Domain separation** is maintained (categories, spectral as separate files)

## Production Usage

In real documents, use:

```latex
\documentclass{scrartcl}
\usepackage{dzg-unified}  % Loads all tiers
\begin{document}
% All macros available
\end{document}
```

Or use a modern preamble:

```latex
\input{koma-article}  % Includes dzg-unified automatically
\begin{document}
% All macros available
\end{document}
```

## Test Coverage

The test documents include examples of:
- All number systems and field extensions
- Calligraphic and fraktur letters
- Mathematical operators (100+ operators)
- Delimiters and brackets
- Algebraic constructions (polynomial rings, power series, quotients)
- Chain/cochain complexes
- Matrices and vectors
- Category theory (categories, functors, limits)
- Spectral sequences (bordism, K-theory, tmf)
- Algebraic geometry (Pic, Spec, cohomology)
- Number theory (p-adics, Galois groups)
- Topology (homology, homotopy groups)
- Differential geometry (tangent bundles, exterior algebra)

All macros successfully tested in the LaTeX compilation.
