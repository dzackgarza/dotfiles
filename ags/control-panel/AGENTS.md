# AGENTS.md

## Project Overview

This is the AGS (Aylur's GTK Shell) configuration directory for the user's Wayland desktop environment, specifically managing widgets, bar components, and the system control center popover panels.

## Tech Stack

- **Framework:** AGS / Astal (Aylur's GTK Shell)
- **Language:** TypeScript (for development/type-checking) & GJS (GObject Introspection / Javascript at runtime)
- **Style:** Vanilla CSS compiled from Sass (`style.scss`)
- **Compilation/Tooling:** `just` (centralized recipes in `Justfile`), `tsc` (TypeScript compiler)

## Operational Philosophy & Code Conventions

### 1. Do NOT Chase External/System-Wide Library Type Warnings
- **The Rule:** Never attempt to fix or chase static compiler warnings or errors originating from system-installed AGS files (such as `/usr/share/ags/js/` or `node_modules` symlinked to GJS system libraries).
- **The Rationale:** These system-level libraries contain internal `.ts` source files with strict type-safety mismatches that the TypeScript compiler (`tsc`) flags under strict project configurations. Because AGS uses GJS under the hood, the runtime executes transpiled JavaScript directly, rendering static compiler warnings in external libraries completely harmless.
- **Actionable Guidance:** When verifying changes with `just typecheck` or `tsc`, ensure that only our local project files (e.g. `src/`, `widget/`, `services/`) are checked or that any local compilation succeeds. If the typecheck command returns non-zero exit codes solely due to system files (like `gnim` under `/usr/share/ags/js/`), **record the failure, ignore it, and proceed with runtime verification**. Do not modify or work around these external libraries.

### 2. UI Modularization & De-duplication
- Keep UI configurations completely dynamic and decoupled.
- Avoid hardcoding provider models, quotas, or layouts. 
- external data sources (e.g. CLI tools like `usage-limits --json` for the LLM Usage popovers) and map layouts dynamically over active records/snapshots.

### 3. State Management
- Utilize AGS accessors, bindings, and polling services for active, responsive states.
- Cleanly handle error snapshot statuses gracefully by displaying user-facing visual alerts rather than silently crashing the bar/widget.

## Key Files

- `app.tsx`: Application entry point.
- `Justfile`: Centralized recipes for the compositor (`run`, `typecheck`).
- `tsconfig.json`: TypeScript compiler settings, configured with loose flags (`strictNullChecks: false`) to minimize transitive system type warnings.
- `services/`: Custom service controllers and fetchers (e.g., `claude-usage-fetcher.ts`).
- `widget/`: UI widgets, overlays, popovers, and layout panels (e.g., `ClaudeUsagePopover.tsx`).
- `style/`: SCSS styling modules.
