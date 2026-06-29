import importlib.util
import sys
import unittest
from pathlib import Path


SCRIPT_PATH = (
    Path(__file__).resolve().parents[1]
    / ".config-sync"
    / "waybar"
    / "scripts"
    / "workspaces-compact.py"
)


def load_module():
    spec = importlib.util.spec_from_file_location("waybar_workspaces_compact", SCRIPT_PATH)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    write_bytecode = sys.dont_write_bytecode
    sys.dont_write_bytecode = True
    try:
        spec.loader.exec_module(module)
    finally:
        sys.dont_write_bytecode = write_bytecode
    return module


class WaybarWorkspacesCompactTest(unittest.TestCase):
    def test_render_payload_uses_numeric_ids_and_window_counts(self):
        module = load_module()

        payload = module.render_payload(
            [
                {"id": 1, "windows": 5, "monitor": "eDP-1"},
                {"id": 2, "windows": 1, "monitor": "eDP-1"},
                {"id": 3, "windows": 1, "monitor": "eDP-1"},
                {"id": 4, "windows": 0, "monitor": "eDP-1"},
                {"id": -98, "windows": 1, "monitor": "eDP-1"},
            ],
            {"id": 3},
        )

        self.assertEqual(
            payload["text"],
            "<span foreground='#cdd6f4'>1</span>"
            "<span foreground='#3e4b59'>:</span>"
            "<span foreground='#ffb454'>5</span>"
            "<span foreground='#3e4b59'> </span>"
            "<span foreground='#cdd6f4'>2</span>"
            "<span foreground='#3e4b59'>:</span>"
            "<span foreground='#ffb454'>1</span>"
            "<span foreground='#3e4b59'> </span>"
            "<span foreground='#11111b' background='#cdd6f4'>3:1</span>"
            "<span foreground='#3e4b59'> </span>"
            "<span foreground='#3e4b59'>4</span>"
            "<span foreground='#3e4b59'> </span>"
            "<span foreground='#3e4b59'>5</span>"
            "<span foreground='#3e4b59'> </span>"
            "<span foreground='#3e4b59'>6</span>"
            "<span foreground='#3e4b59'> </span>"
            "<span foreground='#3e4b59'>7</span>"
            "<span foreground='#3e4b59'> </span>"
            "<span foreground='#3e4b59'>8</span>"
            "<span foreground='#3e4b59'> </span>"
            "<span foreground='#3e4b59'>9</span>"
            "<span foreground='#3e4b59'> </span>"
            "<span foreground='#3e4b59'>10</span>",
        )
        self.assertIn("* 3: 1 windows (eDP-1)", payload["tooltip"])
        self.assertNotIn("-98", payload["tooltip"])
        self.assertEqual(payload["class"], "compact-workspaces")


if __name__ == "__main__":
    unittest.main()
