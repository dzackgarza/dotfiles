# Obsidian MathJax Configuration

This directory contains the maximal MathJax-safe macro subset for use in Obsidian with the better-mathjax plugin.

## Setup

### 1. Symlink mathjax-macros.tex to your Obsidian vault

```bash
ln -s /home/dzack/dotfiles/pandoc/core/obsidian/mathjax-macros.tex \
      /home/dzack/notes/Obsidian/.obsidian/mathjax-macros.tex
```

### 2. Configure better-mathjax plugin

1. Open Obsidian Settings
2. Navigate to "Community Plugins" → "Better MathJax"
3. Set "Custom macro file" to `.obsidian/mathjax-macros.tex`
4. Reload Obsidian

### 3. Test rendering

Create a test note with:

```markdown
# MathJax Test

**Tier 1 macros (simple shortcuts):**
- Number systems: $\ZZ, \QQ, \RR, \CC$
- Calligraphic: $\cA, \cB, \cC$

**Tier 2 and domain macros:**
- Generators: $\gens{a, b, c}$
- Absolute value: $\abs{x}$
- Norm: $\norm{v}$
- Inner product: $\inner{u}{v}$
- Categories: $\Set, \calg, \modsleft{R}$
- Spectra: $\tmf, \MO, \KU$
```

All macros should render correctly.

## What Macros Are Available?

### Tier 1 (Simple, no arguments)
- Number systems: `\ZZ`, `\QQ`, `\RR`, `\CC`, `\FF`, `\PP`, etc.
- Categories: `\Set`, `\Grp`, `\Ring`, `\Mod`, etc.
- Operators: `\Hom`, `\Aut`, `\End`, `\Ext`, `\Tor`, etc.

See `styles/macros/tier1-mathjax-simple.tex` for full list.

### Tier 2 (With arguments, MathJax-safe)
- Delimiters: `\abs{x}`, `\norm{v}`, `\gens{a,b}`, `\bracket{x}`
- Brackets: `\ceiling{x}`, `\floor{x}`
- Inner products: `\inner{u}{v}`
- Complexes: `\complex{C}`, `\cocomplex{C}`
- Function fields: `\fps{x}`, `\functionfield{K}`

See `styles/macros/tier2-mathjax-args.tex` for full list.

### Domain Sources
- Category theory: `\Set`, `\calg`, `\modsleft{R}`, `\gset{G}`
- Spectral sequences and spectra: `\tmf`, `\MO`, `\KU`, `\Suspendpinf`

See `styles/macros/categories.tex` and `styles/macros/spectral.tex` for full lists.

## What Won't Work in Obsidian?

**Tier 3 and 4 macros** (LaTeX-only):
- Complex TeX primitives (`\mathpalette`, `\ooalign`, boxes)
- Package loading and document setup
- TikZ diagrams
- Custom environments

These will only work in full LaTeX/Pandoc documents, not in Obsidian MathJax.

## Adding New Macros

1. Add macro to the appropriate file in `styles/macros/`:
   - `tier1-mathjax-simple.tex` (no args, simple shortcuts)
   - `tier2-mathjax-args.tex` (with args, MathJax-safe)
   - `categories.tex` or `spectral.tex` (domain macros that are MathJax-safe)

2. Macros auto-load in Obsidian on next reload (no need to update this file)

## Troubleshooting

**Macros not rendering:**
- Check that symlink exists: `ls -l ~/.obsidian/mathjax-macros.tex`
- Verify better-mathjax plugin is enabled
- Reload Obsidian (Ctrl+R or Cmd+R)
- Check Obsidian console for errors (Ctrl+Shift+I)

**Some macros work, others don't:**
- Tier 3/4 macros won't work in MathJax (expected)
- Check that macro is actually in a MathJax-compatible source file
- Complex macros with spacing/boxes won't render

**Symlink broken after moving vault:**
- Update symlink to new vault location
- Or copy `mathjax-macros.tex` directly to `.obsidian/` (not recommended)
