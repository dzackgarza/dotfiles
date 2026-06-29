import json
import os
import subprocess
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPT = REPO_ROOT / ".config-sync" / "waybar" / "scripts" / "lid-toggle.py"


class WaybarLidToggleTest(unittest.TestCase):
    def _payload(self, state_dir: Path, *args: str) -> dict:
        output = subprocess.check_output([SCRIPT, "--state-dir", state_dir, *args], text=True)
        return json.loads(output)

    def test_toggle_controls_real_logind_lid_inhibitor(self):
        runtime_dir = tempfile.TemporaryDirectory(prefix="waybar-lid-test-")
        state_dir = Path(runtime_dir.name)
        self.addCleanup(runtime_dir.cleanup)
        self.addCleanup(
            subprocess.run,
            [SCRIPT, "--state-dir", state_dir, "--set", "hibernate"],
            text=True,
            stdout=subprocess.PIPE,
            check=True,
        )

        self.assertEqual(
            self._payload(state_dir, "--status"),
            {
                "text": "lid:hibernate",
                "tooltip": "Lid close action: hibernate\nClick to switch to ignore",
                "class": "hibernate",
            },
        )

        self.assertEqual(
            self._payload(state_dir, "--toggle"),
            {
                "text": "lid:ignore",
                "tooltip": "Lid close action: ignore\nClick to switch to hibernate",
                "class": "ignore",
            },
        )

        inhibitors = json.loads(
            subprocess.check_output(
                [
                    "/usr/bin/systemd-inhibit",
                    "--list",
                    "--json=short",
                    "--what=handle-lid-switch",
                ],
                text=True,
            )
        )
        self.assertIn(
            {
                "who": "waybar-lid-toggle",
                "uid": os.getuid(),
                "user": os.environ["USER"],
                "pid": inhibitors[-1]["pid"],
                "comm": "systemd-inhibit",
                "what": "handle-lid-switch",
                "why": "Waybar lid toggle: ignore lid close",
                "mode": "block",
            },
            inhibitors,
        )

        self.assertEqual(
            self._payload(state_dir, "--toggle"),
            {
                "text": "lid:hibernate",
                "tooltip": "Lid close action: hibernate\nClick to switch to ignore",
                "class": "hibernate",
            },
        )
