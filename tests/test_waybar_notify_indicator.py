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
    def test_render_payload_uses_bell_with_green_zero_count(self):
        module = load_module()

        payload = module.render_payload(
            {
                "text": "0",
                "alt": "none",
                "tooltip": "0 Notifications",
                "class": "none",
            }
        )

        self.assertEqual(
            payload,
            {
                "text": "<span foreground='#aad94c'>󰂚</span>",
                "tooltip": "0 Notifications",
                "class": "none",
            },
        )

    def test_render_payload_uses_amber_for_first_active_notification(self):
        module = load_module()

        payload = module.render_payload(
            {
                "text": "1",
                "alt": "notification",
                "tooltip": "1 Notifications",
                "class": "notification",
            }
        )

        self.assertEqual(
            payload,
            {
                "text": (
                    "<span foreground='#ffb454'>󰂚</span>"
                    "<span foreground='#ffb454' size='x-small' rise='4500'>1</span>"
                ),
                "tooltip": "1 Notifications",
                "class": "notification",
            },
        )

    def test_render_payload_progresses_active_count_toward_red(self):
        module = load_module()

        payload = module.render_payload(
            {
                "text": "50",
                "alt": "notification",
                "tooltip": "50 Notifications",
                "class": "notification",
            }
        )

        self.assertEqual(
            payload,
            {
                "text": (
                    "<span foreground='#f79265'>󰂚</span>"
                    "<span foreground='#f79265' size='x-small' rise='4500'>50</span>"
                ),
                "tooltip": "50 Notifications",
                "class": "notification",
            },
        )

    def test_render_payload_uses_red_when_count_exceeds_one_hundred(self):
        module = load_module()

        payload = module.render_payload(
            {
                "text": "101",
                "alt": "notification",
                "tooltip": "101 Notifications",
                "class": "notification",
            }
        )

        self.assertEqual(
            payload,
            {
                "text": (
                    "<span foreground='#f07178'>󰂚</span>"
                    "<span foreground='#f07178' size='x-small' rise='4500'>101</span>"
                ),
                "tooltip": "101 Notifications",
                "class": "notification",
            },
        )

    def test_render_payload_uses_green_slashed_bell_for_dnd_zero_count(self):
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
                "text": "<span foreground='#aad94c'>󰂛</span>",
                "tooltip": "Do Not Disturb",
                "class": "dnd-none",
            },
        )


if __name__ == "__main__":
    unittest.main()
