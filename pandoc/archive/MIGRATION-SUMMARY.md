# LaTeX Macro Consolidation - Implementation Summary

**Date:** 2025-05-09
**Status:** Phases 1-4, 6 Complete | Phases 5, 7 Remaining

## Overview

Successfully consolidated scattered LaTeX macro files into a clean, tier-organized library structure with clear MathJax compatibility boundaries.

## Completed Work

### Phase 1: New Directory Structure ✅ COMPLETE

Created `lib/` with **2,318 total lines** of organized macros:

#### Tier Files (1,436 lines)
- `tier1-mathjax-simple.tex` (847 lines)
  - Simple MathJax-compatible shortcuts
  - No arguments, only `\mathbb`, `\mathcal`, `\mathsf`, `\mathrm`, `\mathfrak`
  - Examples: `\ZZ`, `\QQ`, `\RR`, `\CC`, `\Hom`, `\Aut`

- `tier2-mathjax-args.tex` (410 lines)
  - Commands with 1-9 arguments (MathJax-compatible)
  - Uses only `\left`, `\right`, `\frac`, `\text`, basic math mode
  - Examples: `\abs{x}`, `\norm{v}`, `\gens{a,b}`, `\inner{u}{v}`

- `tier3-tex-complex.tex` (101 lines)
  - Complex TeX primitives (LaTeX-only, NOT MathJax)
  - Uses `\ooalign`, `\mkern`, `\kern`, spacing hacks
  - Examples: matrices, stacking, complex formatting

- `tier4-preamble.tex` (78 lines)
  - Package-dependent declarations
  - `\DeclareMathOperator`, `\DeclarePairedDelimiter`, `\renewcommand`
  - Requires amsmath, mathtools packages

#### Domain-Specific Files (882 lines)
- `categories.tex` (286 lines) - Category theory
- `spectral.tex` (57 lines) - Spectral sequences
- `tikz.tex` (463 lines) - TikZ styles (consolidated from 3 files)
- `environments.tex` (353 lines) - Theorem environments

#### Documentation
- `lib/README.md` - Tier system guide, decision tree, migration notes

### Phase 2: Unified Style Files ✅ COMPLETE

- `styles/dzg-unified.sty` - Loads all tiers for full LaTeX/Pandoc documents
- `styles/dzg-mathjax.sty` - MathJax subset (tiers 1-2 only) for Obsidian

### Phase 3: TEXINPUTS Update ✅ COMPLETE

- Updated `~/.zshrc` to include `$HOME/.pandoc/lib//` in TEXINPUTS
- Dual support: both `lib/` and `macros/` accessible during migration
- Allows gradual template migration without breaking existing documents

### Phase 4: Modern Preambles ✅ COMPLETE

Created two modern preambles using unified style:

- `preambles/koma-article.tex`
  - KOMA-Script based (replaces `macros/preamble.tex`)
  - For homework, notes, general documents
  - Custom section formatting, headers, footers

- `preambles/ams-article.tex`
  - AMS article based (replaces `macros/preamble_paper.tex`)
  - For journal/conference submissions
  - Standard AMS theorem environments

- `preambles/README.md` - Usage documentation

Both use `\usepackage{dzg-unified}` for all macros.

### Phase 6: Obsidian Integration ✅ COMPLETE

- `obsidian/mathjax-macros.tex` - Loads tiers 1-2 only
- `obsidian/README.md` - Setup instructions
- Ready for better-mathjax plugin via symlink to `.obsidian/mathjax-macros.tex`

## Remaining Work

### Phase 5: Template Migration (Not Started)

6 templates need updating to use `\usepackage{dzg-unified}`:

1. `templates/pandoc_template.tex`
2. `templates/homework_template.tex`
3. `templates/pandoc_paper_template.tex`
4. `templates/pandoc_problem_template.tex`
5. `templates/MakeMeAQual_template.tex`
6. `templates/research_draft.tex`

**Required changes:**
- Replace `\input{preamble.tex}` with `\usepackage{dzg-unified}`
- Remove absolute paths to old macro files
- Test compilation

### Phase 7: Cleanup & Archival (Not Started)

- Remove `macros/` from TEXINPUTS in `.zshrc`
- Move old macro files to `archive/legacy-macros-2025-01-09/`
- Verify templates compile with new structure
- Final testing with actual documents

## Migration Statistics

### Source Files Consolidated
- `macros/latexmacs.tex` (980 lines) → tier files
- `macros/latexmacs_categories.tex` (267 lines) → `categories.tex`
- `macros/latexmacs_spectra.tex` (41 lines) → `spectral.tex`
- `macros/latexmacs_commands.tex` (150 lines) → tier2 and tier3
- `macros/tikz_macros.tex` + `tikzmacros.tex` + `Tikz_Macros.tex` → `tikz.tex`
- `macros/environments.tex` (353 lines) → `environments.tex`

### Final Structure
- **lib/**: 9 files, 2,318 lines of organized macros
- **styles/**: 2 new unified style files
- **preambles/**: 2 modern preambles + README
- **obsidian/**: MathJax integration files

## Key Benefits

1. **Clear MathJax Boundary**
   - Tiers 1-2: Work in LaTeX, Pandoc, and Obsidian MathJax
   - Tiers 3-4: LaTeX/Pandoc only
   - Easy to identify what works where

2. **Single Unified Import**
   - Before: Multiple `\input{latexmacs}`, `\input{preamble_common}`, etc.
   - After: Single `\usepackage{dzg-unified}`

3. **Organized by Purpose**
   - Domain-specific macros separated (categories, spectral, TikZ)
   - Clear tier organization by complexity and compatibility

4. **Well-Documented**
   - README files explain tier system
   - Decision tree for adding new macros
   - Migration notes preserved

5. **Obsidian-Ready**
   - MathJax subset available for mathematical note-taking
   - Clear documentation for setup

## Usage

### In LaTeX Documents

```latex
\documentclass{article}
\usepackage{dzg-unified}  % Loads all tiers + domain macros

\begin{document}
$\ZZ, \QQ, \RR, \CC$  % Tier 1
$\abs{x}, \norm{v}$   % Tier 2
\end{document}
```

### With Modern Preambles

```latex
\input{koma-article}  % Includes dzg-unified automatically

\title{My Document}
\begin{document}
% All macros available
\end{document}
```

### In Obsidian

1. Symlink `obsidian/mathjax-macros.tex` to `.obsidian/mathjax-macros.tex`
2. Configure better-mathjax plugin to load the file
3. Tiers 1-2 macros work in math blocks

## Next Steps

To complete the migration:

1. **Migrate templates (Phase 5)**
   - Update all 6 templates to use `\usepackage{dzg-unified}`
   - Test compilation of each

2. **Final cleanup (Phase 7)**
   - Archive old `macros/` directory
   - Remove `macros/` from TEXINPUTS
   - Test actual documents compile correctly

3. **Create Obsidian symlink**
   ```bash
   ln -s ~/dotfiles/pandoc/obsidian/mathjax-macros.tex \
         ~/notes/Obsidian/.obsidian/mathjax-macros.tex
   ```

## Files Modified

### Created
- `lib/tier1-mathjax-simple.tex` (847 lines)
- `lib/tier2-mathjax-args.tex` (410 lines)
- `lib/tier3-tex-complex.tex` (101 lines)
- `lib/tier4-preamble.tex` (78 lines)
- `lib/categories.tex` (286 lines)
- `lib/spectral.tex` (57 lines)
- `lib/tikz.tex` (463 lines)
- `lib/environments.tex` (353 lines)
- `lib/README.md`
- `styles/dzg-unified.sty`
- `styles/dzg-mathjax.sty`
- `preambles/koma-article.tex`
- `preambles/ams-article.tex`
- `preambles/README.md`
- `obsidian/mathjax-macros.tex`
- `obsidian/README.md`

### Modified
- `~/.zshrc` (added `lib/` to TEXINPUTS)

### To Be Archived (Phase 7)
- `macros/latexmacs.tex`
- `macros/latexmacs_categories.tex`
- `macros/latexmacs_commands.tex`
- `macros/latexmacs_spectra.tex`
- `macros/tikz_macros.tex`
- `macros/tikzmacros.tex`
- `macros/Tikz_Macros.tex`
- `macros/preamble.tex`
- `macros/preamble_paper.tex`
- `macros/preamble_common.tex`
