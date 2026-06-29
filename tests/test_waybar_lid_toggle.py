import json
import os
import subprocess
import tempfile
import time
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPT = REPO_ROOT / ".config-sync" / "waybar" / "scripts" / "lid-toggle.py"


class WaybarLidToggleTest(unittest.TestCase):
    def _payload(self, state_dir: Path, *args: str) -> dict:
        output = subprocess.check_output([SCRIPT, "--state-dir", state_dir, *args], text=True)
        return json.loads(output)

    def _lid_inhibitors(self) -> list[dict]:
        output = ""
        for _ in range(20):
            output = subprocess.check_output(
                [
                    "/usr/bin/systemd-inhibit",
                    "--list",
                    "--json=short",
                    "--what=handle-lid-switch",
                ],
                text=True,
            )
            if output.strip():
                return json.loads(output)
            time.sleep(0.05)
        self.fail(f"waybar lid inhibitor did not appear in logind list output: {output!r}")

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
                "text": "⏾",
                "tooltip": "Lid close action: hibernate\nClick to switch to ignore",
                "class": "hibernate",
            },
        )

        self.assertEqual(
            self._payload(state_dir, "--toggle"),
            {
                "text": "⊘",
                "tooltip": "Lid close action: ignore\nClick to switch to hibernate",
                "class": "ignore",
            },
        )

        inhibitors = self._lid_inhibitors()
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
                "text": "⏾",
                "tooltip": "Lid close action: hibernate\nClick to switch to ignore",
                "class": "hibernate",
            },
        )
