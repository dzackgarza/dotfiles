"""Contract tests for the usage-limits --json CLI output.

Verifies the CLI produces valid JSON matching the UsageCollection schema
that the TypeScript consumer depends on.
"""

import json
import subprocess
from datetime import datetime
from pathlib import Path
from shutil import which

PROJECT_ROOT = Path(__file__).resolve().parent.parent
USAGE_LIMITS_DIR = PROJECT_ROOT.parent.parent / "usage-limits"
UV_BIN = which("uv")
assert UV_BIN is not None, "uv executable not found on PATH"


def _run_usage_limits() -> dict:
    """Run usage-limits --json and return the parsed output."""
    result = subprocess.run(
        [UV_BIN, "run", "--project", str(USAGE_LIMITS_DIR), "usage-limits", "--json"],
        capture_output=True,
        text=True,
        timeout=30,
    )
    if result.returncode != 0:
        raise RuntimeError(
            f"usage-limits --json failed (exit {result.returncode}):\n"
            f"stdout: {result.stdout}\nstderr: {result.stderr}"
        )
    return json.loads(result.stdout)


def test_output_is_valid_json_with_expected_schema():
    """The CLI output must be parseable JSON matching UsageCollection shape."""
    data = _run_usage_limits()

    # Top-level fields
    assert isinstance(data, dict), f"Expected dict, got {type(data).__name__}"
    assert data.get("version") == "1", (
        f"Expected version '1', got {data.get('version')!r}"
    )

    captured_at = data.get("captured_at", "")
    assert isinstance(captured_at, str) and captured_at, (
        f"captured_at must be non-empty string, got {captured_at!r}"
    )
    # Validate ISO 8601 format
    datetime.fromisoformat(captured_at)

    providers = data.get("providers", [])
    assert isinstance(providers, list), (
        f"providers must be a list, got {type(providers).__name__}"
    )
    assert len(providers) > 0, "providers list must not be empty"

    keys_found = {p.get("provider") for p in providers}
    expected_keys = {
        "antigravity",
        "claude",
        "codex",
        "copilot",
        "cursor",
        "kiro",
        "ollama",
        "opencode-go",
        "opencode-zen",
        "qoder",
        "trae",
        "windsurf",
    }
    missing = expected_keys - keys_found
    assert not missing, f"Missing expected providers: {missing}"


def test_every_provider_has_required_fields():
    """Each provider snapshot must have the full ProviderSnapshot schema."""
    data = _run_usage_limits()
    failures = []

    for provider in data["providers"]:
        prov_id = provider.get("provider", "???")

        # Required string fields
        for field in ("provider", "display_name"):
            val = provider.get(field)
            if not isinstance(val, str):
                failures.append(
                    f"{prov_id}: {field} must be a string, got {type(val).__name__}"
                )

        # status must be one of the allowed values
        status = provider.get("status")
        if status not in ("ok", "error", "rate_limited"):
            failures.append(
                f"{prov_id}: status must be 'ok'/'error'/'rate_limited', got {status!r}"
            )

        # rows must be a list of UsageRow
        rows = provider.get("rows", [])
        if not isinstance(rows, list):
            failures.append(f"{prov_id}: rows must be a list")
        else:
            for i, row in enumerate(rows):
                if not isinstance(row.get("identifier"), str):
                    failures.append(f"{prov_id}: rows[{i}].identifier must be a string")
                if not isinstance(row.get("pct_used"), (int, float)):
                    failures.append(f"{prov_id}: rows[{i}].pct_used must be numeric")
                if not isinstance(row.get("is_exhausted"), bool):
                    failures.append(f"{prov_id}: rows[{i}].is_exhausted must be a bool")
                if row.get("reset_at") is not None and not isinstance(
                    row.get("reset_at"), str
                ):
                    failures.append(
                        f"{prov_id}: rows[{i}].reset_at must be string or null"
                    )
                if not isinstance(row.get("time_until_reset"), str):
                    failures.append(
                        f"{prov_id}: rows[{i}].time_until_reset must be a string"
                    )

        # availability must be a list of ModelAvailability
        avail = provider.get("availability", [])
        if not isinstance(avail, list):
            failures.append(f"{prov_id}: availability must be a list")
        else:
            for i, a in enumerate(avail):
                if not isinstance(a.get("name"), str):
                    failures.append(
                        f"{prov_id}: availability[{i}].name must be a string"
                    )
                if not isinstance(a.get("available_now"), bool):
                    failures.append(
                        f"{prov_id}: availability[{i}].available_now must be a bool"
                    )

        # errors must be a list
        errors = provider.get("errors", [])
        if not isinstance(errors, list):
            failures.append(f"{prov_id}: errors must be a list")
        else:
            for i, err in enumerate(errors):
                if not isinstance(err.get("type"), str):
                    failures.append(f"{prov_id}: errors[{i}].type must be a string")
                if not isinstance(err.get("message"), str):
                    failures.append(f"{prov_id}: errors[{i}].message must be a string")

        # metadata must be a dict
        metadata = provider.get("metadata", {})
        if not isinstance(metadata, dict):
            failures.append(f"{prov_id}: metadata must be a dict")

        # account must be string or null
        account = provider.get("account")
        if account is not None and not isinstance(account, str):
            failures.append(f"{prov_id}: account must be string or null")

    assert not failures, "Schema violations:\n" + "\n".join(failures)


def test_pct_used_produces_valid_gtk_fraction():
    """Every pct_used / 100 must be in [0, 1] for Gtk ProgressBar.fraction.

    The Gtk ProgressBar fraction property only accepts values in [0, 1].
    pct_used values exceeding 100 (e.g. trae=100.4653) produce fractions
    above 1.0 and trigger GLib-GObject-CRITICAL warnings.

    This test proves the upstream data includes values that would violate
    the Gtk widget boundary without clamping downstream.
    """
    data = _run_usage_limits()
    failures = []
    for provider in data["providers"]:
        for i, row in enumerate(provider.get("rows", [])):
            fraction = row["pct_used"] / 100
            if fraction < 0 or fraction > 1:
                failures.append(
                    f"{provider['provider']}: rows[{i}].pct_used={row['pct_used']} -> "
                    f"fraction={fraction} (outside [0, 1])"
                )
    assert not failures, (
        "pct_used values that exceed valid Gtk ProgressBar fraction range:\n"
        + "\n".join(failures)
    )


def test_providers_match_provider_icons_map():
    """All providers from usage-limits must have entries in PROVIDER_ICONS."""
    import re

    data = _run_usage_limits()
    tsx_path = PROJECT_ROOT / "src" / "windows" / "control-center.tsx"
    tsx_text = tsx_path.read_text()

    # Extract PROVIDER_ICONS keys from the TypeScript source
    icon_keys: set[str] = set()
    in_block = False
    for line in tsx_text.splitlines():
        stripped = line.strip()
        if stripped.startswith("const PROVIDER_ICONS"):
            in_block = True
            continue
        if in_block:
            if stripped == "}":
                break
            m = re.match(r'^\s*"?(\S+?)"?:\s*"([^"]+)"', stripped)
            if m:
                icon_keys.add(m.group(1).rstrip(","))

    providers_from_cli = {p["provider"] for p in data["providers"]}
    unmapped = providers_from_cli - icon_keys
    assert not unmapped, (
        f"Providers from usage-limits --json without icon mappings: {unmapped}"
    )
