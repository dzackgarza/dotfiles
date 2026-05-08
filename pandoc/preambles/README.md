# Preambles

Modern, consolidated preambles using the unified `dzg-unified.sty` macro package.

## Available Preambles

### `koma-article.tex`
**Use for:** General documents, homework, lecture notes, personal writing

**Features:**
- KOMA-Script `scrartcl` class
- Custom section/subsection formatting
- Fancy headers and footers
- Bibliography with biblatex (alphabetic style)
- Full graphics and TikZ support
- Optimized for readability and modern typography

**Example:**
```latex
\input{koma-article}

\title{My Document}
\author{Your Name}
\date{\today}

\begin{document}
\maketitle

% Your content here

\end{document}
```

### `ams-article.tex`
**Use for:** Journal submissions, conference papers, formal mathematics papers

**Features:**
- AMS `amsart` class (standard for mathematical publications)
- Full AMS theorem environments (numbered by subsection)
- Minimal styling (journal-appropriate)
- 1-inch margins
- Auto-scaling images
- XY-pic diagram support

**Example:**
```latex
\input{ams-article}

\title{A Mathematical Result}
\author{Your Name}

\begin{document}
\maketitle

\begin{abstract}
Abstract text here.
\end{abstract}

% Your content here

\end{document}
```

## Macro Loading

Both preambles load `dzg-unified.sty`, which includes:
- Tier 1: Simple MathJax-compatible shortcuts
- Tier 2: Commands with arguments (MathJax-compatible)
- Tier 3: Complex TeX-specific commands
- Tier 4: Package loading and document setup
- Domain-specific macros (categories, spectral sequences, TikZ)

See `lib/README.md` for details on the tier system.

## Migrating from Old Preambles

**Old:** `\input{preamble.tex}` or `\input{preamble_paper.tex}`

**New:** `\input{koma-article}` or `\input{ams-article}`

The new preambles replace:
- `macros/preamble.tex` → `preambles/koma-article.tex`
- `macros/preamble_paper.tex` → `preambles/ams-article.tex`

## Customization

To customize a preamble:
1. Copy it to your document directory
2. Modify as needed
3. Reference it with `\input{./your-custom-preamble}`

Do not modify the preambles in `preambles/` directly - these are templates.
