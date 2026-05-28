The previous specs left room for two incompatible implementations: “Pandoc owns structure” versus “Flowmark/Marko owns structure.” The pasted transcript shows the exact failure mode: the implementation drifted into Marko regex parsing, then corrected back toward Pandoc AST/custom-writer ownership. The new spec should forbid that ambiguity explicitly. 

# Spec: `pandoc-flowmark`

## One-sentence architecture

**Pandoc owns Markdown structure. Flowmark owns prose formatting only inside Pandoc-approved safe islands. The wrapper writes only after Pandoc validation and idempotence checks pass.**

Pandoc is the semantic authority because its design is reader → native AST → writer, with filters able to modify the intermediate AST. ([Pandoc][1]) Flowmark is used because it already provides the desired Markdown prose behavior: semantic line breaks, smart quotes, ellipses, safe cleanups such as unbold headings, configurable list spacing, CLI use, library use, and TOML configuration. ([GitHub][2])

## Non-negotiable invariants

1. **Pandoc is the only parser for Pandoc Markdown constructs.**
   Fenced divs, bracketed spans, citations, raw TeX, display math, inline math, footnotes, tables, attributes, and metadata blocks are never parsed by custom regex code, Marko extensions, or ad hoc line scanners.

2. **Flowmark must never be trusted as the parser for Pandoc Markdown.**
   Flowmark may format CommonMark-safe prose fragments or an entire document only when a Pandoc-based classifier proves the input is CommonMark-safe for the selected profile.

3. **No Marko Pandoc-extension parser is allowed in v1.**
   Do not add `PandocFencedDivBlock`, `PandocDisplayMathBlock`, or similar Marko elements. That path caused the confusion. It is explicitly out of scope.

4. **Regex is forbidden for structural Markdown recognition.**
   Allowed: trivial byte cleanup such as final newline, trailing-space stripping, or Flowmark’s own internal sentence-boundary heuristics. Flowmark itself documents that its semantic sentence splitting is regex-based; that is acceptable only because it is prose wrapping, not Pandoc structure parsing. ([GitHub][2])

5. **Fail closed.**
   If a block, inline, or subtree cannot be proven safe for Flowmark, leave it to Pandoc/Lua handling. Do not guess.

6. **Never write invalid output.**
   The wrapper writes to disk only after the output parses with Pandoc, passes the configured AST-equivalence check, and is idempotent.

7. **Formatting profiles are explicit.**
   `layout` mode preserves document meaning modulo harmless layout normalization. `cleanup` mode may change text or inline structure, but only through named, whitelisted transformations.

8. **Every blocker becomes an experiment, not an implementation detour.**
   If a model is unsure whether something works, it must create or update a viability experiment record under `docs/formatting/experiments/`, not silently redesign the architecture.

## Architectural decision

The implementation is **not**:

```text
Flowmark/Marko parses Pandoc Markdown
  -> custom regex nodes for fenced divs/math
  -> Pandoc validates afterward
```

The implementation is:

```text
input.md
  -> Pandoc parses with configured markdown extensions
  -> Pandoc AST classifier marks safe prose islands
  -> Flowmark formats only those safe islands
  -> Pandoc Lua writer/filter canonicalizes Pandoc-specific layout
  -> Pandoc reparses output
  -> AST-equivalence/idempotence checks
  -> write
```

Use Pandoc Lua filters/custom writers for AST-level transformations. Pandoc’s custom-writer documentation explicitly supports modifying a document and then delegating rendering to an existing writer via `pandoc.write`. ([Pandoc][3])

## Component ownership table

| Concern                          | Owner                                 | Rule                                                                       |
| -------------------------------- | ------------------------------------- | -------------------------------------------------------------------------- |
| Fenced div parsing               | Pandoc                                | Never regex; handled as `Div` nodes.                                       |
| Fenced div rendering             | Lua writer/filter                     | Canonical delimiter layout.                                                |
| Display math parsing             | Pandoc                                | Handled as `Math(DisplayMath, ...)`.                                       |
| Display math rendering           | Lua writer/filter                     | Canonical `\[`, body, `\]` lines.                                          |
| Paragraph wrapping               | Flowmark                              | Only inside safe prose islands.                                            |
| Sentence-boundary line splitting | Flowmark                              | Allowed as prose heuristic.                                                |
| Smart quotes                     | Flowmark cleanup profile              | Not enabled in strict layout mode.                                         |
| Ellipses                         | Flowmark cleanup profile              | Not enabled in strict layout mode.                                         |
| Unbold headings                  | Flowmark cleanup profile              | Whitelisted AST delta only.                                                |
| List spacing                     | Flowmark, guarded by Pandoc AST check | Must not change tight/loose list semantics unless configured.              |
| Citations                        | Pandoc                                | Flowmark may touch surrounding prose only if citation atomicity is proven. |
| Raw TeX/raw HTML                 | Pandoc/opaque                         | Flowmark must not modify.                                                  |
| Final validation                 | Pandoc                                | Mandatory before write.                                                    |

## Canonical Pandoc-specific formatting rules

### Fenced divs

Pandoc fenced divs are native `Div` blocks. The syntax begins with at least three colons plus attributes and ends with a colon fence; nested divs are supported. Pandoc also notes that unmatched fence lengths are permitted, though different lengths can help visual clarity. ([Pandoc][1])

Canonical rule:

```markdown
:::{.remark}
Content is always on the next line.
:::
```

Required behavior:

```text
Div(attr, blocks, depth):
  opening fence = ":" repeated (3 + depth) + render_attr(attr)
  body = render child blocks
  closing fence = ":" repeated (3 + depth)
  opening fence always on its own line
  content always starts on the next line
  closing fence always on its own line
```

Do not detect `:::` in source text. The formatter sees `Div` nodes only.

### Display math

Pandoc recognizes TeX math and writes Markdown display math using `$$...$$` by default for Markdown-like outputs, while LaTeX output uses `\[...\]`. Therefore the desired `\[...\]` Markdown convention requires a writer/filter override rather than just the stock Pandoc Markdown writer. ([Pandoc][4])

Canonical rule:

```markdown
\[
f(x) = 2
\]
```

Required behavior:

```text
Para([Math(DisplayMath, tex)]):
  emit \[ on its own line
  emit tex body unchanged except outer blank-line trimming
  emit \] on its own line
```

If display math appears embedded in nontrivial inline context, strict mode rejects the file with a clear diagnostic. Permissive mode delegates to Pandoc’s default rendering and records a warning.

## Flowmark integration rule

Flowmark is not optional fluff. It supplies the features the tool actually wants: semantic wrapping, smart quotes, ellipses, cleanups, list spacing, and file/config ergonomics. ([GitHub][2])

But Flowmark is not the structural parser. It is called only in one of these modes:

### Mode A: safe-island mode, default

Pandoc parses the document. The wrapper extracts CommonMark-safe subtrees or block runs, renders each as Markdown, runs Flowmark on that fragment, reparses the fragment with Pandoc, and replaces the original subtree only if the AST delta is allowed.

Safe by default:

```text
Para / Plain with no Citation, Math, RawInline, Span attributes, or custom inlines
Header with simple text/emphasis/code/link content
BulletList / OrderedList only if all items are safe and tightness is preserved
BlockQuote only if all children are safe
```

Unsafe by default:

```text
Div
Span with attributes
Math
Citation
RawBlock / RawInline
CodeBlock with attributes
Table
DefinitionList
Footnote-heavy blocks
LineBlock
Anything involving unknown Pandoc extensions
```

Unsafe does not mean unformatted. It means Flowmark does not touch it; Pandoc/Lua canonicalizers may still format it.

### Mode B: whole-document Flowmark mode, gated

Whole-document Flowmark is allowed only when the Pandoc classifier proves there are no Pandoc-only constructs that Flowmark could misparse. This is useful for ordinary CommonMark/GFM docs.

### Mode C: cleanup mode

Enables Flowmark cleanups that intentionally change text or inline structure:

```text
smartquotes
ellipses
unbold headings
optional list-spacing policy
```

Each cleanup must correspond to a named allowed AST delta. If an observed AST delta is not whitelisted, the write fails.

## Validation model

For every candidate output:

```text
A = Pandoc AST(input)
B = Pandoc AST(output)

layout mode:
  normalize SoftBreak -> Space
  ignore source-position metadata
  require normalized(A) == normalized(B)

cleanup mode:
  normalize SoftBreak -> Space
  apply whitelist of expected cleanup deltas
  require no other AST differences

all modes:
  output must parse
  formatter(output) must equal output byte-for-byte
```

Important: Markdown line wrapping affects Pandoc `SoftBreak` nodes. The AST comparator must normalize `SoftBreak` to `Space` for layout equivalence. It must not normalize `LineBreak`, because hard breaks are semantic.

## Minimal implementation layout

```text
bin/pandoc-flowmark/
  pandoc-flowmark          # Python wrapper; owns pipeline/check/write modes
  writers/
    pandocfmt.lua          # Pandoc custom writer; delegates via pandoc.write
  filters/
    normalize.lua          # optional AST normalizations only
  flowmark_adapter.py      # safe-island extraction and Flowmark calls
  ast_compare.py           # Pandoc JSON AST comparator
  config.example.toml
  tests/
    fixtures/
    golden/
  docs/
    architecture/
      ADR-0001-ownership.md
      ADR-0002-validation.md
    experiments/
      EXP-001-pandoc-writer.md
      EXP-002-flowmark-fragments.md
```

CLI:

```bash
pandoc-flowmark file.md
pandoc-flowmark --check file.md
pandoc-flowmark --stdin
pandoc-flowmark --profile layout file.md
pandoc-flowmark --profile cleanup file.md
pandoc-flowmark --print-ast file.md
pandoc-flowmark --explain file.md
```

Default config:

```toml
profile = "layout"

from = "markdown+fenced_divs+bracketed_spans+tex_math_dollars+tex_math_single_backslash+raw_tex+citations+footnotes+yaml_metadata_block+link_attributes"
to = "markdown+fenced_divs+bracketed_spans+tex_math_dollars+raw_tex+citations+footnotes+yaml_metadata_block+link_attributes"

[flowmark]
enabled = true
mode = "safe-islands"
width = 88
semantic = true
smartquotes = false
ellipses = false
cleanups = false
list-spacing = "preserve"

[pandoc_layout]
canonical_fenced_divs = true
fenced_div_content_next_line = true
canonical_display_math = "single-backslash"
display_math_delimiters_own_lines = true

[validation]
parse_output = true
ast_equivalence = true
normalize_softbreaks = true
idempotence = true
fail_closed = true
```

## Hard “do not do” list

Do not write a Marko extension for Pandoc fenced divs.

Do not regex-match fenced divs.

Do not regex-match display math.

Do not regex-match citations.

Do not run Flowmark over raw Pandoc Markdown unless the Pandoc classifier has approved whole-document mode.

Do not disable AST validation to “make tests pass.”

Do not add cleanup transformations without an explicit AST-delta whitelist.

Do not fork Flowmark until a viability experiment proves the public CLI/library path cannot support safe-island formatting.

Do not fork Pandoc.

## Viability experiments

These are mandatory before implementation decisions that could cause architectural drift. Each experiment gets a permanent Markdown record.

### `EXP-001-pandoc-writer`

Question: Can a Pandoc Lua custom writer walk the AST, replace only `Div` and display-math `Para` nodes with `RawBlock("markdown", ...)`, and delegate the rest to `pandoc.write`?

Success criteria:

```text
- fenced div output is canonical
- display math output is canonical
- non-target blocks are rendered by Pandoc normally
- output reparses under configured extensions
- second formatting pass is byte-identical
```

Record:

```text
docs/formatting/experiments/EXP-001-pandoc-writer.md
```

### `EXP-002-flowmark-fragment-api`

Question: Can Flowmark be called as a library or CLI on small Markdown fragments without requiring whole-document parsing?

Success criteria:

```text
- paragraph fragments format correctly
- heading fragments format correctly
- list fragments format correctly
- links/code spans remain atomic
- Pandoc AST before/after is equivalent modulo SoftBreak
```

Flowmark’s current documentation states that it can be used both as a CLI and as a library, so this is plausible but still must be tested against fragments rather than whole files. ([GitHub][2])

### `EXP-003-safe-island-classifier`

Question: Can the wrapper reliably classify Pandoc AST subtrees as Flowmark-safe?

Success criteria:

```text
- classifier rejects all Pandoc-specific constructs
- classifier accepts simple prose, headings, links, code spans, and simple lists
- every accepted fragment round-trips through Pandoc after Flowmark
- every rejected fragment remains untouched by Flowmark
```

### `EXP-004-inline-pandoc-constructs`

Question: Can inline citations, inline math, bracketed spans, and raw inlines be protected as atomic spans around Flowmark, or must their containing paragraphs be marked unsafe?

Success criteria:

```text
- no citation syntax changes
- no math body changes
- no span attribute changes
- no RawInline changes
- AST equivalence passes
```

Decision rule: if any case is unstable, mark the entire containing block unsafe in v1.

### `EXP-005-list-spacing-and-tightness`

Question: Does Flowmark `--list-spacing=preserve` preserve Pandoc list tightness?

Success criteria:

```text
- tight lists remain tight
- loose lists remain loose
- BulletList/OrderedList item block constructors are unchanged
- no Plain <-> Para changes unless cleanup profile explicitly permits them
```

Flowmark exposes `--list-spacing` with `preserve`, `loose`, and `tight`, but Pandoc AST validation must decide whether the result is acceptable. ([GitHub][2])

### `EXP-006-cleanup-profile-deltas`

Question: Which Flowmark cleanup changes are acceptable in cleanup mode?

Required cases:

```text
**Heading text** -> Heading text
"quotes" -> “quotes”
... -> …
```

Success criteria:

```text
- each accepted change has a named whitelist rule
- each whitelist rule has fixture coverage
- layout mode rejects the same deltas
```

### `EXP-007-nested-fenced-divs`

Question: Does the Lua writer’s depth-based colon fence strategy round-trip nested `Div` nodes?

Success criteria:

```text
- nested Divs parse back to the same nested Div AST
- every opening and closing fence is on its own line
- content starts on the next line
- visual fence lengths are deterministic
```

Pandoc permits nested fenced divs and says fence lengths need not match, but visually distinct lengths may help; the formatter should use deterministic depth-based lengths. ([Pandoc][1])

### `EXP-008-display-math-delimiter-policy`

Question: Does canonical `\[...\]` display math parse under the configured Pandoc extension set and survive round-trip validation?

Success criteria:

```text
- input $$...$$ can canonicalize to \[...\]
- input \[...\] remains \[...\]
- math body is byte-preserved except outer blank lines
- output AST has Math(DisplayMath, same tex)
```

### `EXP-009-whole-document-flowmark-gate`

Question: Is there any safe whole-document Flowmark mode for Pandoc Markdown?

Success criteria:

```text
- classifier approves only CommonMark/GFM-safe documents
- documents containing Div, Citation, Math, RawTeX, bracketed Span, or Pandoc tables are rejected from whole-document mode
- approved documents pass Pandoc AST equivalence after Flowmark
```

Decision rule: if this experiment is flaky, delete whole-document mode from v1.

## Experiment record template

```markdown
# EXP-00N: Title

Date:
Pandoc version:
Flowmark version:
Profile:
Input fixture(s):
Command(s):

## Question

## Expected result

## Observed result

## AST diff

## Decision

Accepted / rejected / needs follow-up.

## Permanent rule added to spec

## Regression tests added
```

## MVP acceptance tests

The MVP is accepted only when these fixtures pass:

```text
01_simple_paragraph_semantic_wrap.md
02_heading_unbold_cleanup_profile.md
03_fenced_div_content_next_line.md
04_nested_fenced_divs.md
05_display_math_bracket_delimiters.md
06_inline_math_untouched.md
07_citation_paragraph_unsafe_or_atomic.md
08_raw_tex_block_untouched.md
09_tight_list_preserved.md
10_loose_list_preserved.md
11_table_untouched_or_pandoc_only.md
12_yaml_metadata_preserved_or_pandoc_canonicalized.md
13_idempotence_all.md
14_check_mode_no_write_on_failure.md
```

## Final implementation rule

When a model starts implementing, the first file it should open is `ADR-0001-ownership.md`. That file should contain exactly this:

```text
Pandoc owns structure.
Flowmark owns prose inside safe islands.
Lua owns Pandoc-specific canonical layout.
Validation owns writes.
Regex does not own Markdown.
Marko does not own Pandoc Markdown.
```

That removes the ambiguity that caused the previous drift.

[1]: https://pandoc.org/MANUAL.html "Pandoc - Pandoc User’s Guide"
[2]: https://github.com/jlevy/flowmark "GitHub - jlevy/flowmark: Modern Markdown formatter with smart typography, line wrapping, and tag support (Python reference implementation) · GitHub"
[3]: https://pandoc.org/custom-writers.html "Pandoc - Creating Custom Pandoc Writers in Lua"
[4]: https://pandoc.org/demo/example33/8.13-math.html "Math"

