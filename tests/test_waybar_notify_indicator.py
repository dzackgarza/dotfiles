import importlib.util
import sys
import unittest
from pathlib import Path


SCRIPT_PATH = (
    Path(__file__).resolve().parents[1]
    / ".config-sync"
    / "waybar"
    / "scripts"
    / "notify-indicator.py"
)


def load_module():
    spec = importlib.util.spec_from_file_location("waybar_notify_indicator", SCRIPT_PATH)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    write_bytecode = sys.dont_write_bytecode
    sys.dont_write_bytecode = True
    try:
        spec.loader.exec_module(module)
    finally:
        sys.dont_write_bytecode = write_bytecode
    return module


class WaybarNotifyIndicatorTest(unittest.TestCase):
    def test_render_payload_uses_bell_with_superscript_count(self):
        module = load_module()

        payload = module.render_payload(
            {
                "text": "9",
                "alt": "notification",
                "tooltip": "9 Notifications",
                "class": "notification",
            }
        )

        self.assertEqual(
            payload,
            {
                "text": "󰂚<span foreground='#ffb454' size='x-small' rise='4500'>9</span>",
                "tooltip": "9 Notifications",
                "class": "notification",
            },
        )

    def test_render_payload_uses_slashed_bell_for_dnd_and_hides_zero_count(self):
        module = load_module()

        payload = module.render_payload(
            {
                "text": "0",
                "alt": "dnd-none",
                "tooltip": "Do Not Disturb",
                "class": "dnd-none",
            }
        )

        self.assertEqual(
            payload,
            {
                "text": "󰂛",
                "tooltip": "Do Not Disturb",
                "class": "dnd-none",
            },
        )


if __name__ == "__main__":
    unittest.main()
