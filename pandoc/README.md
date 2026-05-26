# pandoc

LaTeX styles, pandoc filters, and templates for the dzackgarza publishing
pipeline.

## Styles Architecture

The canonical LaTeX style definitions live in `styles/`. The hierarchy:

- `styles/macros/tikz/` -- unified TikZ macro definitions, split by category
  (layers, nodes, edges, commands, diagrams). The aggregator `tikz.tex` sits one
  level up at `styles/macros/tikz.tex`.
- `styles/macros/tikz/tikzstyles/` -- TikZiT GUI-managed `.tikzstyles` files
- `styles/vendor/` -- files managed by external apps that should not be edited
  directly
- `styles/preambles/` -- shared preamble fragments loaded by the `.sty` entry
  points
- `styles/obsidian/` -- Obsidian-specific style overrides

### The TikZiT Ecosystem

TikZ macros exist in three parallel representations that must be kept in sync:

| File | Format | Managed by | Purpose |
|------|--------|------------|---------|
| `styles/macros/tikz/{nodes,edges,layers,...}.tex` | LaTeX `\tikzset` | Agent/user (canonical) | Primary definitions used in all documents via `dzg-tikz.sty` |
| `styles/vendor/tikzit.sty` | LaTeX `.sty` | TikZiT GUI (auto-generated) | Used when rendering TikZ from within TikZiT; mirrors the canonical macros |
| `styles/macros/tikz/tikzstyles/*.tikzstyles` | TikZiT native format | TikZiT GUI | Native format for the GUI style editor; also mirrors the canonical set |

**Important:** `tikzit.sty` is NOT a standard LaTeX style file. TikZiT is a GUI
application that natively manages styles in `.tikzstyles` files, not `.sty`
files. The `.sty` is a LaTeX-readable mirror generated so that documents
loading `\usepackage{tikzit}` get the same styles available inside the GUI.
TikZiT writes this file for rendering purposes -- it is a vendor artifact, not
a hand-authored package.

The canonical definitions live in `styles/macros/tikz/`. The `.tikzstyles` file
and `tikzit.sty` are secondary mirrors that must be manually updated when the
canonical definitions change.

### TikZiT GUI Limitations

TikZiT provides a GUI-based style editor, but it does not support the full
range of PGF/TikZ features. Styles defined using features outside the GUI's
supported set (arbitrary `\tikzset` keys, complex styling, etc.) will render
correctly in the final PDF but may not display properly or may be invisible
inside the TikZiT GUI editor.

This is a fundamental limitation of the GUI, not a configuration or setup issue.

### Ongoing Maintenance

The `.tikzstyles` file and `tikzit.sty` must be manually kept in sync with the
canonical macros whenever node styles, edge styles, or utility commands are
added, removed, or changed. There is no automated sync mechanism. The process:

1. Edit the canonical `.tex` files in `styles/macros/tikz/`.
2. Manually mirror the changes into `styles/vendor/tikzit.sty`.
3. Manually mirror the changes into
   `styles/macros/tikz/tikzstyles/*.tikzstyles` (TikZiT format).
4. Test by compiling a document that uses the affected styles.

## Future Work

### Bespoke TikZ Style Editor

The long-term plan is to build a standalone GUI editor for TikZ style files
that addresses the limitations of TikZiT's built-in style manager. This editor
would:

- Read, parse, and display styles defined with the full range of PGF/TikZ
  features (not just the subset TikZiT's GUI exposes)
- Support manual (text-editor) edits to style files and reflect them in the
  GUI
- Provide a live preview renderer for node and edge styles
- Support the `.tikzstyles` file format natively
- Act as the canonical source of truth for style definitions, with export to
  both the unified `macros/tikz/*.tex` format and the `tikzit.sty` vendor
  mirror

Until this editor exists, all three representations must be maintained manually.
