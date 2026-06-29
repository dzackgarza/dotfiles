import json
import os
import subprocess
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPT = REPO_ROOT / ".config-sync" / "waybar" / "scripts" / "lid-toggle.py"


class WaybarLidToggleTest(unittest.TestCase):
    def _payload(self, env: dict[str, str], *args: str) -> dict:
        output = subprocess.check_output([SCRIPT, *args], env=env, text=True)
        return json.loads(output)

    def test_toggle_controls_real_logind_lid_inhibitor(self):
        with tempfile.TemporaryDirectory(prefix="waybar-lid-test-") as runtime_dir:
            env = os.environ.copy()
            env["XDG_RUNTIME_DIR"] = runtime_dir

            self.assertEqual(
                self._payload(env, "--status"),
                {
                    "text": "lid:hibernate",
                    "tooltip": "Lid close action: hibernate\nClick to switch to ignore",
                    "class": "hibernate",
                },
            )

            self.addCleanup(
                subprocess.run,
                [SCRIPT, "--set", "hibernate"],
                env=env,
                text=True,
                stdout=subprocess.PIPE,
                check=True,
            )

            self.assertEqual(
                self._payload(env, "--toggle"),
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
                self._payload(env, "--toggle"),
                {
                    "text": "lid:hibernate",
                    "tooltip": "Lid close action: hibernate\nClick to switch to ignore",
                    "class": "hibernate",
                },
            )
