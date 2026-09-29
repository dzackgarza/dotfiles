# AGENT Notes for Hyprland Configs in `~/.config/hypr/confs`

Scope: everything under this directory, especially `windowrules.conf` and other Hyprland config fragments.

The goal of this file is to document a **reliable, reproducible debugging procedure** for Hyprland config changes, with a focus on the 0.53+ window rule and layer rule syntax.

## Source of truth

- Treat the official Hyprland wiki as the primary reference:
  - Window rules: https://wiki.hypr.land/Configuring/Window-Rules/
  - Variables / misc options: https://wiki.hypr.land/Configuring/Variables/
- Do not rely on third‑party blogs or “guides” for syntax; if they disagree with the wiki **or with Hyprland’s own parser**, the wiki + parser win.

## Mandatory debugging steps for config edits

When you touch any Hyprland config in this tree:

1. **Check for syntax errors via Hyprland itself**
   - Run: `hyprctl configerrors`
   - Interpret the output as the single ground truth for whether the config is valid.
   - Common pattern after 0.53:
     - `invalid field float: missing a value` → the `float` effect now expects a value (e.g. `float on`).
     - `invalid field center: missing a value` → the `center` effect also expects a value (`center on`).

2. **Probe syntax with `hyprctl keyword` before editing many lines**
   - Use small, disposable rules to learn what the parser accepts:
     - `hyprctl keyword windowrule 'match:class testclass, float'`  
       → should fail with “missing a value”.
     - `hyprctl keyword windowrule 'match:class testclass, float on'`  
       → should succeed (`ok`).
     - `hyprctl keyword windowrule 'match:class testclass, center on'`  
       → should succeed.
     - `hyprctl keyword windowrule 'match:class testclass, size 60% 80%'`  
       → should succeed.
     - `hyprctl keyword windowrule 'match:class testclass, opacity 0.8 0.5'`  
       → should succeed.
     - `hyprctl keyword windowrule 'match:class testclass, workspace 3'`  
       → should succeed.
   - For layer rules, probe similarly:
     - `hyprctl keyword layerrule 'blur on, match:namespace waybar'`
     - `hyprctl keyword layerrule 'ignore_alpha 0, match:namespace waybar'`
   - Only after confirming the correct shape (e.g. `float on` vs `float`) should you propagate that pattern into the config files.

3. **Rewrite rules using the new props + effects model**
   - Old `windowrulev2` lines like:  
     `windowrulev2 = float, class:^(kitty)$, title:(update)`  
     become:  
     `windowrule = match:class ^(kitty)$, match:title (update), float on`
   - General mapping:
     - `class:REGEX` → `match:class REGEX`
     - `title:REGEX` → `match:title REGEX`
     - `initialTitle:REGEX` → `match:initial_title REGEX`
     - `tag:foo*` → `match:tag foo*`
   - Negative matches:
     - Old `title:negative:(REGEX)` → `match:title negative:(REGEX)`
   - Effects:
     - Boolean‑like: `float`, `center`, etc. → now require an explicit value (`float on`, `center on`).
     - Others (e.g. `size 60% 80%`, `opacity 1.0 0.8`, `workspace 3`) keep their argument shapes.
   - Layer rules:
     - Old: `layerrule = blur,notifications`  
       New: `layerrule = blur on, match:namespace notifications`
     - Old: `layerrule = ignorezero,rofi`  
       New: `layerrule = ignore_alpha 0, match:namespace rofi`

4. **Re‑run `hyprctl configerrors` after edits**
   - The target state is **no output** for the modified files.
   - If errors remain:
     - Use the exact file + line reported to narrow the edit.
     - Prefer a minimal local fix (one rule) over broad rewrites.

5. **Check options with `hyprctl getoption`**
   - Before asserting that a config key exists or is valid, probe it:
     - `hyprctl getoption 'misc:new_window_takes_over_fs'`
   - If Hyprland reports it as unknown or missing, do **not** add it blindly; re‑check the wiki and release notes.

## Honesty / integrity rules (local to this tree)

- Never claim that a config “passes syntax” without first running `hyprctl configerrors` and seeing no errors.
- When there is a mismatch between:
  - your expectations,
  - the wiki, and
  - `hyprctl`’s actual output,
  always treat `hyprctl` as the final arbiter and adjust to it.
- If you previously asserted that a given syntax was valid and `hyprctl` later contradicts that, explicitly surface that earlier assertion as false, correct it, and then update the config.

## Editing discipline (in addition to global AGENTS)

- Limit changes to the smallest possible set of rules that fix the reported errors.
- Prefer:
  - probing with `hyprctl keyword`,
  - then updating a **single** rule,
  - then re‑running `hyprctl configerrors`,
  over bulk mechanical conversions.
- Do not introduce unrelated stylistic changes (re‑ordering, re‑grouping rules) in the same edit as a syntax fix.

