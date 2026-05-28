Corrected spec below. The core correction is: **this is a source-preserving personal formatter, not a general Pandoc Markdown pretty-printer.** Flowmark owns prose formatting. Pandoc is a semantic guard/tooling source, not the final source emitter. The uploaded “Algebraic Spaces” block is fixture 001, and the formatter must return it byte-for-byte unchanged. It already records the failures to avoid: `:::` becoming `::::`, wikilinks being escaped, link targets being percent-encoded, math being rearranged, and prose being width-wrapped.  

# Spec: `zmdfmt`

## Purpose

`zmdfmt` formats Zack’s Pandoc/Obsidian-flavored Markdown according to a growing set of literal examples.

The formatter is not intended to support all Markdown, all Pandoc extensions, all nesting patterns, or all documents in the world. It should do a small number of style-preserving transformations, using existing tools where they help, and it should refuse to invent behavior without a fixture.

The source of truth is:

```text
tests/fixtures/*/before.md
tests/fixtures/*/after.md
```

A behavior exists only if a before/after pair pins it down.

## Central architectural decision

Use this architecture:

```text
input markdown
  -> protect byte-sensitive regions
  -> segment into prose zones and opaque zones
  -> run Flowmark on approved prose zones
  -> run tiny style passes with fixture coverage
  -> restore protected regions byte-for-byte
  -> optional Pandoc validation/smoke checks
  -> compare against expected output in tests
```

Do **not** use this architecture:

```text
input markdown
  -> Pandoc AST
  -> Pandoc Markdown writer
  -> postprocess damage
```

The reason is already demonstrated by the failing fixture: Pandoc’s Markdown writer changed the source in ways that are wrong for this formatter, including fence length, wikilinks, links with spaces, math layout, and line wrapping. 

Pandoc is still useful. It can parse Pandoc Markdown, supports Lua filters/custom writers, and can serve as a validation or experimentation tool. But the final emitter for v0 must be source-preserving text, not the stock Pandoc Markdown writer. Pandoc custom writers can call `pandoc.write`, and Lua filters are built into Pandoc, but those are tools for isolated experiments and semantic checks, not permission to rewrite the whole file through Pandoc’s writer. ([Pandoc][1])

Flowmark is mandatory for prose behavior because it already supplies the desired Markdown formatting features: semantic line breaks, smart quotes, ellipses, safe cleanups, list-spacing controls, CLI use, library use, and TOML configuration. ([GitHub][2])

## Hard invariants

1. **Fixture-first.** No new formatting behavior without a literal `before.md` and `after.md`.

2. **Exact tests.** The primary test is always:

```bash
zmdfmt tests/fixtures/NNN_name/before.md > actual.md
diff -u tests/fixtures/NNN_name/after.md actual.md
```

No AST equivalence test replaces this.

3. **The formatter must preserve unknown syntax.** If a construct is not explicitly owned by a pass, it must remain byte-for-byte unchanged.

4. **Wikilinks are opaque.** Anything of the form `[[...]]` is protected before any tool sees it and restored byte-for-byte afterward. Do not strip it, escape it, normalize it, or reinterpret it.

5. **Math is opaque unless a fixture says otherwise.** Inline math, display math, TeX macros, and raw TeX bodies are protected before prose formatting. The uploaded fixture’s display math is already valid style and must remain unchanged.

6. **No arbitrary line-length wrapping.** Width-based wrapping is forbidden. Line length is an editor concern. The only allowed prose breaking is Flowmark-style semantic wrapping.

7. **`:::` is the default fenced-div delimiter.** Do not introduce depth-based fence growth. Do not emit `::::` unless a literal fixture requires `::::`.

8. **Pandoc’s Markdown writer is not the final emitter in v0.** It has already shown too large a blast radius.

9. **Regex is not a Markdown parser.** Regex may be used only for trivial, isolated byte protection or one-line lexical recognition, with fixture coverage. It must not own Markdown structure.

10. **No Marko Pandoc parser in v0.** Do not build a Marko extension for fenced divs, math, citations, or Pandoc syntax. That path makes agents spiral.

11. **Small modules only.** Each pass owns one behavior and has its own fixtures. A change to math formatting should not affect wikilinks, lists, fenced divs, or prose wrapping.

12. **Fail closed.** If a region cannot be safely formatted, leave it unchanged.

## Known style ledger, v0

These are known requirements from the current fixture and this conversation.

### Fenced divs

Accepted and preserved:

```markdown
:::{.example title="Algebraic Spaces"}
content
:::
```

Pandoc fenced divs begin with at least three colons plus attributes, so `:::` is a valid and normal baseline. There is no v0 rule that lengthens fences by nesting depth. ([Pandoc][3])

Current rule:

```text
Preserve existing ::: fenced div delimiters unless a fixture says to change them.
If a fixture asks to fix same-line content, fix only that shape.
Never invent ::::.
```

Example future fixture, only if desired:

```markdown
# before
:::{.remark} Content.
:::

# after
:::{.remark}
Content.
:::
```

But this rule does not imply rewriting already-correct divs.

### Wikilinks

Accepted and preserved:

```markdown
[[algebraic space|Algebraic spaces]]
```

Rule:

```text
Protect wikilinks before Flowmark, Pandoc, or any cleanup pass.
Restore them byte-for-byte.
```

No escaping:

```markdown
\[\[algebraic space\|Algebraic spaces\]\]
```

No conversion to ordinary Markdown links.

No stripping to display text.

### Markdown links with spaces

Accepted and preserved:

```markdown
[étale sheaves](étale sheaves)
```

Rule:

```text
Do not percent-encode local note links.
```

Forbidden output:

```markdown
[étale sheaves](étale%20sheaves)
```

### Math

Accepted and preserved from fixture:

```markdown
\[  
\mathcal{S}_{\leq 0} \da \ts{\text{Discrete spaces}}
.\]
```

Rule:

```text
Protect math blocks and inline math before prose formatting.
Do not trim spaces, move delimiters, split closing delimiters, or rewrite TeX unless a fixture explicitly requires it.
```

The earlier abstract rule “display delimiters always get their own line” is now demoted to “candidate style, pending fixtures.” The uploaded fixture is stronger evidence of actual style.

### Prose wrapping

Accepted and preserved:

```markdown
Think of these as [étale sheaves](étale sheaves) of sets (think functor of points), identified as discrete spaces:
```

This line is long, but it is a single semantic unit. The formatter must not break it merely because of length.

Rule:

```text
Use Flowmark semantic wrapping.
Do not use width wrapping.
Do not ask Pandoc’s writer to reflow paragraphs.
```

### Correct no-op fixture

Fixture `001_noop_algebraic_spaces`:

```markdown
:::{.example title="Algebraic Spaces"}
[[algebraic space|Algebraic spaces]], e.g. $\PP^n$.
Think of these as [étale sheaves](étale sheaves) of sets (think functor of points), identified as discrete spaces:
\[  
\mathcal{S}_{\leq 0} \da \ts{\text{Discrete spaces}}
.\]
Every component is contractible, so there are no higher homotopy groups and we think of these as 0-truncated spaces.
:::
```

`before.md` and `after.md` are identical. This is the first regression test. 

## Implementation shape

Use a small Python wrapper plus Flowmark plus isolated protectors/passes:

```text
zmdfmt/
  zmdfmt.py
  flowmark_runner.py

  protect/
    wikilinks.py
    math.py
    code_fences.py
    raw_blocks.py

  segment/
    blocks.py
    prose_zones.py

  passes/
    fenced_div_content_next_line.py
    heading_cleanups.py
    list_spacing.py
    final_newline.py

  validate/
    pandoc_smoke.py

  docs/
    style-ledger.md
    experiments/

  tests/
    fixtures/
      001_noop_algebraic_spaces/
        before.md
        after.md
      002_semantic_sentence_wrap/
        before.md
        after.md
      ...
```

The wrapper should be boring:

```python
def format_text(src: str) -> str:
    protected = protect_all(src)
    zones = segment(protected.text)

    for zone in zones:
        if zone.kind == "prose":
            zone.text = run_flowmark_semantic(zone.text)
        else:
            zone.text = zone.text

    text = join(zones)
    text = run_enabled_style_passes(text)
    text = restore_all(text, protected)
    text = ensure_final_newline(text)
    return text
```

The default enabled passes should be minimal:

```text
1. protect wikilinks
2. protect math
3. protect code fences
4. run Flowmark semantic prose formatting only where safe
5. restore protected regions
6. ensure final newline
```

Everything else waits for a fixture.

## Flowmark integration

Flowmark is the prose formatter, not an optional afterthought.

Required Flowmark behavior:

```text
semantic wrapping: enabled
width wrapping: disabled
smart quotes: configurable, initially fixture-gated
ellipses: configurable, initially fixture-gated
unbold headings: configurable, initially fixture-gated
list spacing: configurable, initially fixture-gated
```

The formatter must not run Flowmark over the whole file blindly. It should run Flowmark only over zones that are safe after protection.

Safe v0 prose zone:

```text
ordinary paragraph text after wikilinks, math, code, and raw regions are masked
ordinary headings after protected spans are masked
simple list item prose after protected spans are masked
```

Unsafe v0 zone:

```text
code fences
math blocks
raw TeX blocks
tables
YAML frontmatter
unknown block syntax
anything inside a protected placeholder
```

Unsafe zones are preserved.

## Pandoc role

Pandoc is a guard and experiment tool.

Allowed uses:

```text
- parse smoke tests on Pandoc-compatible fixtures
- experiments for whether a candidate transform preserves semantics
- optional AST checks after masking wikilinks and other non-Pandoc-native syntax
- Lua filters for isolated semantic inspection
```

Forbidden use in v0:

```text
- feed the entire document to Pandoc’s Markdown writer and use that as final output
- rely on Pandoc writer output for source preservation
- repair Pandoc writer damage afterward
```

A permanent experiment should record the demonstrated blast radius:

```text
EXP-005-pandoc-writer-blast-radius
Decision: Pandoc Markdown writer is not the final emitter for v0.
Reason: fixture 001 changed fence length, wikilinks, link targets, math, and prose wrapping.
```

## Test harness

The test harness must be this simple:

```bash
#!/usr/bin/env bash
set -euo pipefail

for dir in tests/fixtures/*; do
  [ -d "$dir" ] || continue
  tmp="$(mktemp)"
  zmdfmt "$dir/before.md" > "$tmp"
  diff -u "$dir/after.md" "$tmp"
  rm -f "$tmp"
done
```

No AST oracle in the main correctness path.

Optional guard tests may exist separately:

```text
tests/guards/pandoc-smoke.sh
tests/guards/idempotence.sh
```

But the main formatter contract is literal source transformation.

## Initial fixture suite

Start with 10–20 examples. Do not implement a rule until the fixture exists.

### 001: already-correct algebraic spaces block

`before.md == after.md`.

Covers:

```text
:::{.example ...}
wikilink alias
inline math
Markdown link target with space
display math block
long semantic prose line
no width wrapping
```

### 002: semantic sentence wrapping

Example shape:

```markdown
# before
This is the first sentence. This is the second sentence.

# after
This is the first sentence.
This is the second sentence.
```

Only add once Flowmark configuration is verified.

### 003: no width wrapping

Example shape:

```markdown
# before
This is a deliberately long sentence with many mathematical words and references that should remain one line because it is one semantic sentence.

# after
This is a deliberately long sentence with many mathematical words and references that should remain one line because it is one semantic sentence.
```

### 004: wikilink preservation

```markdown
# before
See [[spectral sequence|spectral sequences]].

# after
See [[spectral sequence|spectral sequences]].
```

### 005: Markdown note link target with spaces

```markdown
# before
See [étale sheaves](étale sheaves).

# after
See [étale sheaves](étale sheaves).
```

### 006: inline math preservation

```markdown
# before
For $f\colon X\to Y$, write $\fib_y(f)$.

# after
For $f\colon X\to Y$, write $\fib_y(f)$.
```

### 007: display math preservation

Use the exact display math style you actually want. For now, fixture 001 says the current style is accepted.

### 008: fenced div same-line content, if desired

Only add if this is a real desired rewrite:

```markdown
# before
:::{.remark} Content is on the same line.
:::

# after
:::{.remark}
Content is on the same line.
:::
```

### 009: heading cleanup

Only if desired:

```markdown
# before
## **Schemes**

# after
## Schemes
```

### 010: smart quotes

Only if desired:

```markdown
# before
"Affine schemes" are basic.

# after
“Affine schemes” are basic.
```

### 011: ellipses

Only if desired:

```markdown
# before
This continues...

# after
This continues…
```

### 012: list spacing

Fixture must decide your actual style:

```markdown
# before
- First item.
- Second item.

# after
- First item.
- Second item.
```

or loose-list style if that is what you want.

### 013: code fence untouched

````markdown
# before
```python
print("[[not a wikilink]]")
````

# after

```python
print("[[not a wikilink]]")
```

````

### 014: raw TeX untouched

```markdown
# before
\newcommand{\PP}{\mathbb{P}}

# after
\newcommand{\PP}{\mathbb{P}}
````

### 015: YAML frontmatter untouched or normalized

Do not decide abstractly. Add the fixture.

## Module rules

Each module gets one job.

`protect/wikilinks.py`:

```text
Input: source text
Output: source text with wikilinks replaced by opaque placeholders
Restores: exact original bytes
Allowed to know: wikilink byte spans
Forbidden to know: Markdown paragraphs, lists, fenced divs
```

`protect/math.py`:

```text
Protects inline math, display math, and TeX blocks.
Does not normalize TeX.
Does not trim whitespace.
```

`segment/prose_zones.py`:

```text
Finds regions that can safely go to Flowmark.
Never edits text.
```

`flowmark_runner.py`:

```text
Calls Flowmark with the chosen semantic-only configuration.
Does not protect syntax itself.
Does not run on opaque zones.
```

`passes/fenced_div_content_next_line.py`:

```text
Only fixes fixture-approved same-line fenced-div content.
Does not implement nested-div theory.
Does not change ::: to ::::.
```

`passes/final_newline.py`:

```text
Ensures exactly one final newline.
This is allowed as trivial byte cleanup.
```

## Agent instructions

Agents implementing this must follow these rules:

```text
1. Add or inspect the fixture first.
2. Run the test and see the diff.
3. Change the smallest module that owns that behavior.
4. Re-run all fixtures.
5. Do not add generality unless a fixture requires it.
6. Do not use Pandoc’s Markdown writer as the final output.
7. Do not add nesting-depth logic.
8. Do not parse Markdown with regex.
9. Do not touch wikilinks except through the wikilink protector.
10. Do not touch math except through the math protector.
11. Do not enable Flowmark options without a fixture showing the desired output.
12. When uncertain, create an experiment record instead of redesigning the architecture.
```

## Viability experiments

Experiments are for blockers only. They are permanent records, not exploratory edits hidden in code.

Store them here:

```text
docs/experiments/EXP-001-flowmark-semantic-only.md
docs/experiments/EXP-002-wikilink-protection.md
...
```

Template:

```markdown
# EXP-00N: Title

Date:
Tool versions:
Fixtures used:

## Question

## Command

## Observed diff

## Decision

## Rule added to spec

## Tests added
```

### EXP-001: Flowmark semantic-only mode

Question:

```text
Can Flowmark be configured or called so that it performs semantic wrapping without arbitrary width wrapping?
```

Success:

```text
fixture 001 is unchanged
semantic sentence fixture changes only at sentence boundaries
long one-sentence fixture is not wrapped by length
```

Failure decision:

```text
If Flowmark cannot do this directly, isolate or adapt only its semantic wrapping component.
Do not replace it with width wrapping.
```

### EXP-002: Wikilink protection

Question:

```text
Can wikilinks be masked before Flowmark/Pandoc and restored byte-for-byte?
```

Success:

```text
[[algebraic space|Algebraic spaces]] survives exactly
[[spectral sequence|spectral sequences]] survives exactly
wikilink-like text inside code fences is not touched
```

### EXP-003: Math protection

Question:

```text
Can inline math and display math be protected and restored byte-for-byte?
```

Success:

```text
$\PP^n$ survives exactly
fixture 001 display math survives exactly
no whitespace inside math is trimmed
```

### EXP-004: Flowmark on protected prose zones

Question:

```text
After masking wikilinks and math, can Flowmark safely format prose zones?
```

Success:

```text
ordinary prose gets semantic wrapping
protected placeholders survive and restore correctly
non-prose zones remain unchanged
```

### EXP-005: Pandoc writer blast radius

Question:

```text
Can Pandoc’s Markdown writer be used as the final emitter?
```

Known answer:

```text
No for v0.
```

Record the already observed diff:

```text
::: -> ::::
[[...]] -> \[\[...\]\]
(etale sheaves) -> (etale%20sheaves)
math whitespace/layout changed
long semantic lines width-wrapped
```

This experiment prevents future agents from rediscovering the same bad path.

### EXP-006: Fenced div same-line content

Question:

```text
Should zmdfmt rewrite :::{.remark} content onto the next line?
```

Success:

```text
Only the exact fixture shape changes.
Already-correct fixture 001 remains unchanged.
No depth logic is introduced.
```

### EXP-007: Cleanups

Question:

```text
Which Flowmark cleanups are actually wanted?
```

Separate fixtures required for:

```text
smart quotes
ellipses
unbold headings
list spacing
```

No fixture means no cleanup.

### EXP-008: Pandoc validation with wikilinks

Question:

```text
Can Pandoc validation be useful after masking wikilinks and other personal syntax?
```

Success:

```text
validation catches broken Pandoc Markdown in compatible regions
validation does not force source rewrites
validation does not reject valid personal syntax after masking
```

Failure decision:

```text
Keep Pandoc validation optional and advisory.
Do not let it drive formatting.
```

## Final rule of the project

Put this in `docs/architecture.md` and at the top of the implementation guide:

```text
This is Zack’s source-preserving Markdown formatter.

Fixtures define behavior.
Flowmark formats prose semantically.
Protected syntax is restored byte-for-byte.
Pandoc validates; it does not emit final source.
No arbitrary width wrapping.
No general-purpose Pandoc pretty-printing.
No ::: depth games.
No behavior without before.md and after.md.
```

That should stop the agent failure mode: the model should not try to infer a universal formatter. It should add one literal example, write one narrow pass, and preserve everything else.

[1]: https://pandoc.org/custom-writers.html?utm_source=chatgpt.com "Creating Custom Pandoc Writers in Lua"
[2]: https://github.com/jlevy/flowmark?utm_source=chatgpt.com "jlevy/flowmark: Modern Markdown formatter with smart ..."
[3]: https://pandoc.org/demo/example33/8.18-divs-and-spans.html?utm_source=chatgpt.com "8.18 Divs and Spans"
