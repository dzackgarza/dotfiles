# Legacy Macro Files - Archived 2025-01-09

These files were archived as part of the LaTeX macro consolidation project.
All content has been migrated to the new `lib/` directory structure.

## Archived Files

### Main Macro Files
- `latexmacs.tex` (980 lines) → Migrated to `lib/tier*.tex` (1,436 lines total)
- `latexmacs_categories.tex` (267 lines) → Migrated to `lib/categories.tex` (286 lines)
- `latexmacs_spectra.tex` (41 lines) → Migrated to `lib/spectral.tex` (57 lines)
- `latexmacs_commands.tex` (150 lines) → Migrated to `lib/tier2-mathjax-args.tex` and `lib/tier3-tex-complex.tex`

### TikZ Files
- `tikz_macros.tex` (394 lines) → Migrated to `lib/tikz.tex`
- `tikzmacros.tex` (5 lines) → Merged into `lib/tikz.tex`
- `Tikz_Macros.tex` (30 lines) → Not migrated (commented code)

### Preamble Files
- `preamble.tex` (315 lines) → Replaced by `preambles/koma-article.tex`
- `preamble_paper.tex` (179 lines) → Replaced by `preambles/ams-article.tex`
- `preamble_common.tex` (212 lines) → Content migrated to tier files
- `preamble_paper.pre` → Legacy file

### Environment Files
- `environments.tex` (353 lines) → Copied to `lib/environments.tex`

## Migration Details

All macros were categorized into a 4-tier system:

- **Tier 1:** Simple MathJax-compatible shortcuts (847 lines)
- **Tier 2:** Commands with arguments (MathJax-compatible) (410 lines)
- **Tier 3:** Complex TeX-specific commands (101 lines)
- **Tier 4:** Package-dependent declarations (78 lines)

See `/home/dzack/dotfiles/pandoc/MIGRATION-SUMMARY.md` for complete details.

## Restoration

If you need to restore these files:

```bash
cd /home/dzack/dotfiles/pandoc
cp archive/legacy-macros-2025-01-09/filename.tex macros/
```

However, the new structure is recommended as it provides:
- Clear MathJax compatibility boundaries
- Better organization by purpose
- Single unified import (`\usepackage{dzg-unified}`)
- Obsidian integration support

## New Structure

Use these instead:
- `\usepackage{dzg-unified}` - All macros for LaTeX/Pandoc
- `\input{koma-article}` - Full KOMA-Script preamble
- `\input{ams-article}` - Full AMS article preamble
- `obsidian/mathjax-macros.tex` - MathJax subset for Obsidian
