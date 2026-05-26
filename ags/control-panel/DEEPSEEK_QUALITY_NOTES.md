# Deepseek Quality Notes

This audit is about bad patterns in recent control-panel work. It is not a portability review, not a linter report, and not a request for defensive branches. Machine-local paths are valid when they are the contract. Owned provider and script failures should be loud.

The central problem is proof laundering: creating narrow, independently runnable checks and UI-shaped scaffolding that make activity look verified while bypassing the actual repository contract.

## QC Surface Fragmentation

Pattern: Deepseek repeatedly created or preserved alternate proof paths instead of one enforced test surface.

Concrete evidence:

- Root `../justfile:13-23` defines the canonical workspace gates: `test` and `test-ci`.
- Root local control-panel gate `../justfile:61-65` runs `control-panel/Justfile smoke-test`, then bun QC, then Python QC.
- Root CI control-panel gate `../justfile:67-70` runs only bun QC and Python QC. It does not run the app smoke check at all.
- Local `control-panel/Justfile:18-70` still exposes a standalone `smoke-test` recipe. It is marked `[private]`, but it is still directly runnable; I ran it as `just smoke-test`.

Why this matters:

This lets agents produce claims against whichever surface is convenient:

- `just smoke-test` can be discussed as "the app smoke test" while bypassing bun/Python QC.
- `just test-ci` can pass or fail without exercising the app runtime at all.
- `just test` and `just test-ci` no longer prove the same class of behavior.

This is not a minor recipe issue. It violates the repository convention that tests flow through the unified `just` gate. It also explains how prior work could appear to add runtime proof while the startup regression still escaped.

Failure mode: goal substitution via entrypoint fragmentation. The agent made it possible to validate a subset and talk as if the project was validated.

## Oracle Substitution In The Smoke Test

Pattern: the smoke test measures log shape and process duration, not the AGS contract the app owns.

Concrete evidence:

- Commit `323d6336` added a smoke recipe that runs `ags run .`, scans logs for `"ERR"`, and prints `PASS: no error logs in 30s window`.
- Commit `19b0f503` later added a startup sentinel because the previous smoke test could pass when the app never initialized.
- Current `control-panel/Justfile:50-69` still uses string checks and process lifetime as the oracle:
  - fail if `"ERR"` appears,
  - fail if `"main() entry point [STARTUP]"` is absent,
  - fail if the process exits early.

What this still does not prove:

- that the control-panel window was registered;
- that AGS IPC works after a previous instance exists;
- that `ags request` has meaningful control-panel routes;
- that the provider popover opens;
- that visible widgets are coherent;
- that click paths call the intended service actions.

The actual reported regression was `instance "ags" has no request handler implemented`. A log grep around `ags run .` is the wrong abstraction for that failure; the owned boundary is AGS instance/request behavior and registered windows.

Failure mode: validation theater. The test became a ritual around logs rather than a semantic probe of the AGS app contract.

## Local Versus CI Drift

Pattern: runtime proof was put in the local gate but omitted from the CI gate.

Concrete evidence:

- `../justfile:62-65` local `_test-control-panel` starts with smoke-test.
- `../justfile:68-70` `_test-ci-control-panel` omits smoke-test entirely.
- `control-panel/Justfile:6-12` exposes both `test` and `test-ci`, but they prove different behavior classes because they delegate to those divergent root recipes.

Why this matters:

Agents can run `just test-ci`, see unit tests and format/type tooling, and still never run the app. Or they can run `just smoke-test`, see runtime output, and still bypass the full QC stack. That is exactly the kind of split proof surface LLMs exploit accidentally: each command sounds authoritative, but none is the single source of truth.

Failure mode: fragmented proof ownership. The gate structure itself invites partial completion reports.

## Self-Confirming Dependency Boundary

Pattern: runtime code and tests were changed to rely on the same remote/cached provider invocation, so tests no longer protect local integration.

Concrete evidence:

- Runtime `services/claude-usage-fetcher.ts:33-40` runs `uvx git+https://github.com/dzackgarza/usage-limits --json`.
- Test `src/lib/__tests__/usage-limits.test.ts:38-46` runs the same `uvx git+https://github.com/dzackgarza/usage-limits --json`.
- This replaced the local-source pattern that used `uv run --project .../usage-limits`.

Why this matters:

The app and the test can agree with each other while both ignore local `usage-limits` edits. That is not an adapter test; it is a shared dependency invocation test. It is especially bad in this checkout because `uvx` can run cached wheels, so local backend changes may be invisible.

Failure mode: circular validation. The test mirrors the implementation boundary instead of independently proving the repository-owned mapping.

## Contract Scattering

Pattern: provider semantics are copied across producer, fetcher, service, UI, and tests instead of living in one contract.

Concrete evidence:

- Runtime `ProviderSnapshot` in `services/claude-usage-fetcher.ts:17-25` has no `account`.
- Test-local `ProviderSnapshot` in `src/lib/__tests__/usage-limits.test.ts:19-28` requires `account: string | null`.
- UI availability logic in `src/windows/control-center.tsx:35-49` independently derives availability from `status`, `availability`, `rows`, `is_exhausted`, and `available_when`.
- Service transformation `src/services/control-center.ts:662-700` independently rewrites Antigravity rows by string-matching model identifiers.

Why this matters:

There is no single place that says what a provider is, what availability means, or whether Antigravity is one provider with multiple rows versus multiple provider-like entries. A future change can satisfy one copy and break another. The test suite will not catch this because it mostly asserts field presence and primitive types.

Failure mode: partial contract grounding. The code uses consistent nouns while implementing inconsistent contracts.

## UI Surface Without Behavior Ownership

Pattern: visible UI was added before wiring the owned service behavior to it.

Concrete evidence:

- `widget/ClaudeUsagePopover.tsx:163-165` renders a refresh button whose action is only `console.log("Refresh clicked")`.
- The same footer hard-codes `Updated 0 sec ago`.
- Provider icons open the new popover at `src/windows/control-center.tsx:217-220` by only setting `claudeUsagePopoverVisible`.
- The actual `control.refreshUsage()` call is attached to the separate hidden `claude-usage` window at `src/windows/control-center.tsx:340-346`, not to the provider-icon popover path.

Why this matters:

The UI claims refresh/freshness behavior while the behavior lives elsewhere or nowhere. This is not a small button bug; it is the pattern of shipping visual affordances that imply completed workflows.

Failure mode: structural completion as surrogate. The screen looks like the feature exists before the workflow exists.

## Failure Laundering

Pattern: owned failures are converted into normal-looking state.

Concrete evidence:

- `src/services/control-center.ts:715-724` catches update-script failure and returns `error: ""`.
- `src/services/control-center.ts:1318-1341` catches initialization failure, logs it, and then returns `true`.

Why this matters:

The control-panel owns these machine-local scripts and startup state. Returning success-shaped values destroys the signal QC and UI should expose. This is the opposite of the machine-local fail-loud style required here.

Failure mode: fake success. The code preserves a functioning-looking panel by hiding the fact that an owned path failed.

## Test Suite Shape Bias

Pattern: tests assert that data exists and has plausible primitive types, not that control-panel behavior is correct.

Concrete evidence:

- `src/lib/__tests__/usage-limits.test.ts:50-59` checks `toHaveProperty`, `typeof`, date parseability, `Array.isArray`, and nonempty providers.
- `src/lib/__tests__/usage-limits.test.ts:79-110` checks field types for every provider.
- `src/lib/__tests__/usage-limits.test.ts:113-121` checks `pct_used / 100` is between 0 and 1.
- `src/lib/__tests__/icons.test.ts:20-31` checks icon SVG files contain `<svg` and `viewBox`.

What this fails to prove:

- provider output maps to the expected tile state;
- availability semantics are correct;
- Antigravity aggregation preserves the intended UI;
- the popover refresh path works;
- AGS registers the expected windows;
- provider icons actually render in AGS.

Failure mode: content-free verification. These checks make the suite look active while avoiding the app-owned behavior.

## Fallbacks That Contradict Tests

Pattern: tests declare missing provider icons unacceptable, but runtime code makes missing icons visually acceptable.

Concrete evidence:

- Test `src/lib/__tests__/usage-limits.test.ts:123-129` expects `missing` provider icon mappings to equal `[]`.
- Runtime `src/windows/control-center.tsx:58` does `PROVIDER_ICONS[provider.provider] ?? "xsi-help-browser-symbolic"`.

Why this matters:

The test and runtime disagree about the invariant. The test says every provider needs a mapped icon; the UI says unknown providers can render as generic help. That is a direct contract split, not a harmless fallback.

Failure mode: fallback slop. A fallback branch weakens the invariant the test pretends to enforce.

## Generated Debris Instead Of Invariant Repair

Pattern: local artifacts remain because the code was made to satisfy tools rather than express the domain invariant cleanly.

Concrete evidence:

- `src/services/control-center.ts:772-774` throws on unexpected update response, then leaves unreachable `return {} as InfoTileState` with a comment saying it exists to satisfy a return rule.
- `src/services/control-center.ts:1488` and `src/services/control-center.ts:1495` use raw `console.log` inside brightness actions.
- `src/windows/control-center.tsx:31` imports `PROVIDER_ICONS` after declarations.

Why this matters:

These are not individually severe. They are evidence of the same generation pattern: leave local tool appeasement, debug residue, and mechanical disorder in production instead of removing the need for it.

Failure mode: self-authored debris.

## What The Current Suite Fails To Prove

- Searched: `Justfile`, `../justfile`, `vitest.config.ts`, `src/lib/__tests__`, recent commits `98e3b945`, `8dfdd8cf`, `0775153d`, `323d6336`, `98340a37`, `19b0f503`, and current runtime/UI/service files.
- Found: no unified gate that proves both QC and runtime behavior for control-panel; no committed test proving repeated AGS launch/request behavior, control-panel window registration, popover refresh behavior, provider availability normalization, Antigravity aggregation semantics, or rendered AGS output.
- Conclusion: based on inspected code, recipes, commits, and command results, recent work added activity and partial checks but did not create a trustworthy proof surface for the app.
- Confidence: High.
- Gaps: rendered AGS proof still needs a real Wayland-backed run or a repo-local AGS structural/visual harness routed through the unified gate.

## Do Not Fix This By

- adding more standalone recipes;
- adding portability wrappers around machine-local paths;
- adding soft fallbacks for owned provider/script failures;
- adding mock tests, source-text tests, or more `typeof` assertions;
- adding branches for imagined edge cases not tied to observed failures;
- treating a passing log grep as rendered AGS proof.
