# 🤖 LLM Onboarding & Project Guide: Mathematics Dissertation

## 👋 Welcome, LLM Research Assistant

You are an advanced mathematics research assistant. Your mission is to help complete a high-quality mathematics dissertation efficiently and to a high academic standard. You will:

- 🧠 Parse, analyze, and audit both the visual PDF output and the semantic content of the thesis.
- 📝 Suggest, implement, and check improvements in clarity, correctness, and rigor.
- 🔍 Use the checklists below to guide your work, focusing on the highest priority tasks first.
- 🤝 Collaborate with human and AI project workers, documenting your findings and actions.

**Remember:**

- The true source is markdown in the `sections/` directory.
- All scripts and checks should be implemented in the `audits/` directory.
- Macros and custom commands may be defined in the `packages/` directory.

## 🗂️ Project Structure & Key Directories

- `sections/` — 📄 Markdown source files (edit here)
- `outputs/` — 🏗️ Generated LaTeX, stripped markdown, and build artifacts
- `packages/` — 📦 Custom LaTeX packages/macros
- `audits/` — 🛠️ Audit scripts, onboarding, and TODOs

## 🏗️ Sub-Projects: Two Pillars of Auditing

The audit and review process is divided into two complementary sub-projects:

### 🖼️ Visual PDF Parsing & Auditing

Focus: Appearance, layout, and visual integrity of the generated PDF.

#### Visual PDF Auditing TODOs

- [ ] ✏️ No typos, grammar, or language errors (run spellcheck/grammar tools on PDF text)
- [ ] 🖼️ All figures, tables, and equations are clear, legible, and properly formatted
- [ ] 🔗 All figures/tables/equations are referenced in the text
- [ ] 🚫 No duplicate or missing labels for figures, tables, or equations
- [ ] ✅ All cross-references (\ref, \cite) resolve correctly in the PDF
- [ ] ❌ No broken, missing, or incorrect cross-references (figures, tables, sections, citations)
- [ ] 🏷️ All sections have clear introductions and conclusions
- [ ] 📏 All formatting guidelines (margins, fonts, etc.) are met
- [ ] ➗ No overly long or complex equations without explanation
- [ ] 🆔 No ambiguous variable names or notation in visual output
- [ ] 📚 All appendices and supplementary material are complete
- [ ] 👀 Regularly build and visually inspect the PDF output for layout and formatting issues
- [ ] Detect overfull/underfull boxes by parsing LaTeX log (visible layout errors)
- [ ] Detect text that is too small to read (PDF font size scan)
- [ ] Detect large vertical whitespace/gaps (PDF whitespace scan)
- [ ] Detect possible misaligned equations (PDF scan for off-center math)
- [ ] Detect overflowing images or tables (PDF scan for content outside page bounds)
- [ ] Check for inconsistent citation style (PDF text scan)
- [ ] Flag images with a high degree of visual similarity (potential duplicates in separate files)
- [ ] Find unnumbered or unreferenced equations/theorems (PDF text scan for eqn/theorem environments and cross-references)
- [ ] Detect orphaned/stranded captions (captions separated from figures/tables)
- [ ] Detect low-resolution or non-vector images (PDF image scan)
- [ ] Detect missing figure/table numbers or captions
- [ ] Check for very short or very long sections (PDF text/structure scan)
- [ ] Check for missing PDF metadata (title, author, keywords)
- [ ] Check for color contrast issues in figures (PDF image scan)

## 🧩 Semantic Text-Level Auditing

Focus: Logical, mathematical, and textual content at the source level (markdown and LaTeX).

### Semantic Auditing TODOs

- [ ] 🗂️ Generate index of all logical units: definitions, theorems, propositions, lemmas, etc. (all named "amsthm" environments)
- [ ] 📊 Count number of **proved** theorems/lemmas/propositions as percentage of all, number of **cited** theorems as percentage of all, etc.
- [ ] 📖 Bibliography tools: check for missing/unused entries, ensure all bibliography entries are cited
- [ ] ❓ Check for undefined terms, symbols, or notation (especially in math)
- [ ] $\mathbb{M}$ Ensure all mathematical expressions are in math mode (`$...$`)
- [ ] ⬇️ Punctuate all equations as part of sentences
- [ ] 🔤 Use standard notation for variables, functions, and operators
- [ ] 🏷️ All theorems, lemmas, and definitions are cited and referenced
- [ ] ⏩ No forward references to equations/theorems
- [ ] 🧾 All claims are cited or proven
- [ ] 🧮 All proofs are complete and logically sound
- [ ] 🔄 Consistent use of notation (scalars, vectors, matrices, etc.)
- [ ] 🅱️ Consistent use of bold/italic/math font for math objects
- [ ] ⚙️ Use `\operatorname{}` or `\DeclareMathOperator` for named functions
- [ ] 🔁 Use `\newcommand` for repeated expressions
- [ ] 📝 All limitations and future work are discussed
- [ ] 🧑‍🔬 All related work and prior art are addressed
- [ ] 🔡 All acronyms and abbreviations are defined at first use
- [ ] 🧪 All code, data, and results are reproducible (low priority)
- [ ] 📏 All units and dimensions are correct and consistent (note: this is pure math, low priority)
- [ ] Detect duplicate citations (same reference cited with multiple keys or entries)
- [ ] Detect inconsistent citation keys for the same work (e.g., Smith2020 vs. Smith:2020)
- [ ] Check for inconsistent or ambiguous mathematical notation (symbol usage across the document)
- [ ] Flag undefined technical terms (terms used but not defined in the text)
- [ ] Find labels (\label{}) that are never referenced (\ref, \eqref, etc.)
- [ ] Find theorems/lemmas/propositions that are never cited in the text
- [ ] Flag proper names (e.g., mathematicians, theorems) mentioned without a literature citation
- [ ] Detect bibliography entries that are never cited
- [ ] Detect citations in the text that do not correspond to any bibliography entry
- [ ] Check for inconsistent theorem/lemma/proposition numbering or naming
- [ ] Flag use of deprecated or discouraged LaTeX packages/commands

## 🛠️ Implementation Notes & Recommended Tools (General)

- All scripts and checks to be implemented in the `audits/` directory
- Focus on actionable, visible errors first (high priority)
- Implementation should remain simple and not require deep NLP or ML

**Recommended Command-Line Tools:**

- [PyMuPDF (fitz)](https://pymupdf.readthedocs.io/en/latest/) 🧩: PDF parsing, text and layout extraction (Python CLI/scriptable)
- [pdfminer.six](https://pdfminersix.readthedocs.io/en/latest/) 📄: Advanced PDF text extraction (Python CLI/scriptable)
- [pdftotext (poppler-utils)](https://poppler.freedesktop.org/) ⚡: Fast PDF to plain text conversion (`pdftotext` CLI)
- [Ghostscript](https://www.ghostscript.com/) 👻: PDF rendering, image extraction, and DPI checks (`gs` CLI)
- [pdftk](https://www.pdflabs.com/tools/pdftk-the-pdf-toolkit/) 🛠️: PDF metadata and structure inspection (`pdftk` CLI)
- [poppler-utils](https://poppler.freedesktop.org/) 🧰: PDF utilities (`pdfimages`, `pdfinfo`, `pdftotext`, etc. CLI)
- LaTeX log parsers (custom Python or regex) 📝: Overfull/underfull box detection (scriptable)
- [re (Python regex)](https://docs.python.org/3/library/re.html) 🔎: Pattern matching for references, citations, and notation (scriptable)
- [PIL/Pillow](https://python-pillow.org/) 🖼️: Image analysis (resolution, format; Python CLI/scriptable)
- [PyPDF2](https://pypdf2.readthedocs.io/en/latest/) 📑: PDF metadata and structure (Python CLI/scriptable)
- [spellchecker (e.g., pyspellchecker)](https://pyspellchecker.readthedocs.io/en/latest/) 📝: Optional for section/caption spellcheck (Python CLI/scriptable)
- [Mathpix CLI & API](https://mathpix.com/) 🤖: PDF/image to LaTeX/Markdown conversion, OCR, equation extraction (CLI/API)
- [JabRef](https://www.jabref.org/) 📚: BibTeX reference manager (CLI import/export, fetches from arXiv, MathSciNet, Google Scholar, etc.)
- [Zotero CLI tools](https://github.com/retorquere/zotero-cli) 📖: Command-line access to Zotero libraries (for citation management)

> **Note:** All tools above are scriptable or have CLI interfaces suitable for automation by LLMs in a terminal environment. Prefer these for all automated or batch tasks.

## 🌐 Scholarly Databases for Mathematics (General)

LLMs and project workers can use these databases to search for mathematical literature, preprints, and reviews:

- [arXiv](https://arxiv.org/) 📄: Preprints in mathematics, physics, and more
- [MathSciNet](https://mathscinet.ams.org/) 🔬: Reviews and bibliographic data for mathematical research (American Mathematical Society)
- [zbMATH Open](https://zbmath.org/) 📚: Abstracts and reviews of pure and applied mathematics
- [Google Scholar](https://scholar.google.com/) 🔎: Broad scholarly search, citation indexing
- [Project Euclid](https://projecteuclid.org/) 📘: Journals in mathematics and statistics
- [JSTOR](https://www.jstor.org/) 📖: Digitized back issues of scholarly journals
- [Scopus](https://www.scopus.com/) 🌍: Abstract and citation database (broad scientific coverage)
- [Web of Science](https://www.webofscience.com/) 🌐: Citation index for scientific literature
- [SIAM Journals](https://www.siam.org/publications/journals) 🧮: Society for Industrial and Applied Mathematics
- [MathWorld](https://mathworld.wolfram.com/) 🌏: Interactive mathematics encyclopedia

> **Tip:** Many of these databases can be searched using LLM MCP tools or by asking the user to perform a search and provide results.

## 📚 Citation Management: Zotero & Local Database (General)

- The user maintains a **local Zotero database** for citations and references.
- LLMs should attempt to query this Zotero database for sources, or ask the user to perform a query and provide the results.
- For BibTeX integration, use [Better BibTeX for Zotero](https://retorque.re/zotero-better-bibtex/) for auto-syncing.
- JabRef can also fetch references from arXiv, MathSciNet, Google Scholar, and more.

## 🏆 Best Practices & Tips (General)

- 🧠 Parse and dedicate files in `outputs/` to memory, especially files matching `*_stripped.{tex,md}` and `Dissertation.tex`.
- 📦 Be aware of macros and commands defined in `packages/`.
- 📝 Make all content edits in the markdown files in `sections/`.
- 🔄 Use version control for all changes (already set up).
- 🤖 Use and improve audit scripts in `audits/` to automate checks and reporting.
- 🏗️ Run build scripts to generate and check output regularly.
- 🗒️ Document all major changes and findings in the changelog or commit messages.
- 📋 Use this onboarding guide and the audit checklist above as your reference.
- 🎯 Focus on high-priority audit tasks first to ensure correctness and academic rigor.
- 🤖 Automate repetitive checks and reporting wherever possible.
- 👀 Use the audit scripts in `audits/` to catch issues early and often.
- 💬 Communicate findings and progress clearly in commit messages or project notes.

## 🌟 Your contributions are vital to the success of this dissertation. Refer to this guide and the audit checklist throughout your work. Let's make this thesis exceptional

## 📑 Mathematics Thesis Audit TODOs (Strict Advisor Priorities)

### 🎓 Advisor's Rationale

Mathematical rigor, logical soundness, and scholarly integrity are paramount. Visual and typographical issues are only relevant after the mathematics is flawless. Typos and grammar, while not tolerated, are not the first concern unless they obscure mathematical meaning.

## 🧩 SEMANTIC TEXT-LEVEL AUDITING (HIGHEST PRIORITY)

*Focus: Mathematical rigor, logical soundness, and scholarly standards.*

1. [ ] 🧮 All proofs are complete, correct, and fully justified—no hand-waving, no gaps.
2. [ ] 🧾 All claims are cited or proven.
3. [ ] 🏷️ All theorems, lemmas, and definitions are cited and referenced.
4. [ ] 🗂️ Generate index of all logical units: definitions, theorems, propositions, lemmas, etc. (all named "amsthm" environments)
5. [ ] 📊 Count number of **proved** theorems/lemmas/propositions as percentage of all, number of **cited** theorems as percentage of all, etc.
6. [ ] ⏩ No forward references to equations/theorems.
7. [ ] ❓ Check for undefined terms, symbols, or notation (especially in math).
8. [ ] 🔤 Use standard, unambiguous notation for variables, functions, and operators.
9. [ ] 🔄 Consistent use of notation (scalars, vectors, matrices, etc.).
10. [ ] 🅱️ Consistent use of bold/italic/math font for math objects.
11. [ ] ⚙️ Use `\operatorname{}` or `\DeclareMathOperator` for named functions.
12. [ ] 🔁 Use `\newcommand` for repeated expressions.
13. [ ] $\mathbb{M}$ Ensure all mathematical expressions are in math mode (`$...$`).
14. [ ] ⬇️ Punctuate all equations as part of sentences.
15. [ ] Detect duplicate citations (same reference cited with multiple keys or entries).
16. [ ] Detect inconsistent citation keys for the same work (e.g., Smith2020 vs. Smith:2020).
17. [ ] Check for inconsistent or ambiguous mathematical notation (symbol usage across the document).
18. [ ] Flag undefined technical terms (terms used but not defined in the text).
19. [ ] Find labels (`\label{}`) that are never referenced (`\ref`, `\eqref`, etc.).
20. [ ] Find theorems/lemmas/propositions that are never cited in the text.
21. [ ] Flag proper names (e.g., mathematicians, theorems) mentioned without a literature citation.
22. [ ] Detect bibliography entries that are never cited.
23. [ ] Detect citations in the text that do not correspond to any bibliography entry.
24. [ ] Check for inconsistent theorem/lemma/proposition numbering or naming.
25. [ ] Flag use of deprecated or discouraged LaTeX packages/commands.
26. [ ] 📖 Bibliography tools: check for missing/unused entries, ensure all bibliography entries are cited.
27. [ ] 🧑‍🔬 All related work and prior art are addressed.
28. [ ] 📝 All limitations and future work are discussed.
29. [ ] 🔡 All acronyms and abbreviations are defined at first use.
30. [ ] 🧪 All code, data, and results are reproducible (low priority).
31. [ ] 📏 All units and dimensions are correct and consistent (note: this is pure math, low priority).

## 🖼️ VISUAL PDF PARSING & AUDITING (SECONDARY PRIORITY)

*Focus: Visual integrity, cross-referencing, and typographical correctness.*

1. [ ] 🚫 No duplicate or missing labels for figures, tables, or equations.
2. [ ] ✅ All cross-references (`\ref`, `\cite`) resolve correctly in the PDF.
3. [ ] ❌ No broken, missing, or incorrect cross-references (figures, tables, sections, citations).
4. [ ] 🔗 All figures/tables/equations are referenced in the text.
5. [ ] 🖼️ All figures, tables, and equations are clear, legible, and properly formatted.
6. [ ] ➗ No overly long or complex equations without explanation.
7. [ ] 🆔 No ambiguous variable names or notation in visual output.
8. [ ] Detect overfull/underfull boxes by parsing LaTeX log (visible layout errors).
9. [ ] Detect possible misaligned equations (PDF scan for off-center math).
10. [ ] Detect overflowing images or tables (PDF scan for content outside page bounds).
11. [ ] Find unnumbered or unreferenced equations/theorems (PDF text scan for eqn/theorem environments and cross-references).
12. [ ] Detect orphaned/stranded captions (captions separated from figures/tables).
13. [ ] Detect missing figure/table numbers or captions.
14. [ ] Detect text that is too small to read (PDF font size scan).
15. [ ] Detect large vertical whitespace/gaps (PDF whitespace scan).
16. [ ] Detect low-resolution or non-vector images (PDF image scan).
17. [ ] Check for inconsistent citation style (PDF text scan).
18. [ ] Flag images with a high degree of visual similarity (potential duplicates in separate files).
19. [ ] Check for very short or very long sections (PDF text/structure scan).
20. [ ] Check for missing PDF metadata (title, author, keywords).
21. [ ] Check for color contrast issues in figures (PDF image scan).
22. [ ] ✏️ No typos, grammar, or language errors (run spellcheck/grammar tools on PDF text).
23. [ ] 🏷️ All sections have clear introductions and conclusions.
24. [ ] 📏 All formatting guidelines (margins, fonts, etc.) are met.
25. [ ] 📚 All appendices and supplementary material are complete.
26. [ ] 👀 Regularly build and visually inspect the PDF output for layout and formatting issues.

### 🛠️ Implementation Notes & Recommended Tools (Visual Audit)

- All scripts and checks to be implemented in the `audits/` directory
- Focus on actionable, visible errors first (high priority)
- Implementation should remain simple and not require deep NLP or ML

**Recommended Command-Line Tools:**

- [PyMuPDF (fitz)](https://pymupdf.readthedocs.io/en/latest/) 🧩: PDF parsing, text and layout extraction (Python CLI/scriptable)
- [pdfminer.six](https://pdfminersix.readthedocs.io/en/latest/) 📄: Advanced PDF text extraction (Python CLI/scriptable)
- [pdftotext (poppler-utils)](https://poppler.freedesktop.org/) ⚡: Fast PDF to plain text conversion (`pdftotext` CLI)
- [Ghostscript](https://www.ghostscript.com/) 👻: PDF rendering, image extraction, and DPI checks (`gs` CLI)
- [pdftk](https://www.pdflabs.com/tools/pdftk-the-pdf-toolkit/) 🛠️: PDF metadata and structure inspection (`pdftk` CLI)
- [poppler-utils](https://poppler.freedesktop.org/) 🧰: PDF utilities (`pdfimages`, `pdfinfo`, `pdftotext`, etc. CLI)
- LaTeX log parsers (custom Python or regex) 📝: Overfull/underfull box detection (scriptable)
- [re (Python regex)](https://docs.python.org/3/library/re.html) 🔎: Pattern matching for references, citations, and notation (scriptable)
- [PIL/Pillow](https://python-pillow.org/) 🖼️: Image analysis (resolution, format; Python CLI/scriptable)
- [PyPDF2](https://pypdf2.readthedocs.io/en/latest/) 📑: PDF metadata and structure (Python CLI/scriptable)
- [spellchecker (e.g., pyspellchecker)](https://pyspellchecker.readthedocs.io/en/latest/) 📝: Optional for section/caption spellcheck (Python CLI/scriptable)
- [Mathpix CLI & API](https://mathpix.com/) 🤖: PDF/image to LaTeX/Markdown conversion, OCR, equation extraction (CLI/API)
- [JabRef](https://www.jabref.org/) 📚: BibTeX reference manager (CLI import/export, fetches from arXiv, MathSciNet, Google Scholar, etc.)
- [Zotero CLI tools](https://github.com/retorquere/zotero-cli) 📖: Command-line access to Zotero libraries (for citation management)

> **Note:** All tools above are scriptable or have CLI interfaces suitable for automation by LLMs in a terminal environment. Prefer these for all automated or batch tasks.

### 🌐 Scholarly Databases for Mathematics (Visual Audit)

LLMs and project workers can use these databases to search for mathematical literature, preprints, and reviews:

- [arXiv](https://arxiv.org/) 📄: Preprints in mathematics, physics, and more
- [MathSciNet](https://mathscinet.ams.org/) 🔬: Reviews and bibliographic data for mathematical research (American Mathematical Society)
- [zbMATH Open](https://zbmath.org/) 📚: Abstracts and reviews of pure and applied mathematics
- [Google Scholar](https://scholar.google.com/) 🔎: Broad scholarly search, citation indexing
- [Project Euclid](https://projecteuclid.org/) 📘: Journals in mathematics and statistics
- [JSTOR](https://www.jstor.org/) 📖: Digitized back issues of scholarly journals
- [Scopus](https://www.scopus.com/) 🌍: Abstract and citation database (broad scientific coverage)
- [Web of Science](https://www.webofscience.com/) 🌐: Citation index for scientific literature
- [SIAM Journals](https://www.siam.org/publications/journals) 🧮: Society for Industrial and Applied Mathematics
- [MathWorld](https://mathworld.wolfram.com/) 🌏: Interactive mathematics encyclopedia
- [MacTutor History of Mathematics](https://mathshistory.st-andrews.ac.uk/) 🏛️: Biographies and history

> **Tip:** Many of these databases can be searched using LLM MCP tools or by asking the user to perform a search and provide results.

### 📚 Citation Management: Zotero & Local Database (Visual Audit)

- The user maintains a **local Zotero database** for citations and references.
- LLMs should attempt to query this Zotero database for sources, or ask the user to perform a query and provide the results.
- For BibTeX integration, use [Better BibTeX for Zotero](https://retorque.re/zotero-better-bibtex/) for auto-syncing.
- JabRef can also fetch references from arXiv, MathSciNet, Google Scholar, and more.

### 🏆 Best Practices & Tips (Visual Audit)

- 🧠 Parse and dedicate files in `outputs/` to memory, especially files matching `*_stripped.{tex,md}` and `Dissertation.tex`.
- 📦 Be aware of macros and commands defined in `packages/`.
- 📝 Make all content edits in the markdown files in `sections/`.
- 🔄 Use version control for all changes (already set up).
- 🤖 Use and improve audit scripts in `audits/` to automate checks and reporting.
- 🏗️ Run build scripts to generate and check output regularly.
- 🗒️ Document all major changes and findings in the changelog or commit messages.
- 📋 Use this onboarding guide and the audit checklist above as your reference.
- 🎯 Focus on high-priority audit tasks first to ensure correctness and academic rigor.
- 🤖 Automate repetitive checks and reporting wherever possible.
- 👀 Use the audit scripts in `audits/` to catch issues early and often.
- 💬 Communicate findings and progress clearly in commit messages or project notes.

## 🏛️ Remember: Mathematical substance and rigor come first. Visual polish is only meaningful when the mathematics is impeccable
