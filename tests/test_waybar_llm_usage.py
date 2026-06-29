import copy
import importlib.util
import sys
import unittest
from datetime import datetime, timezone
from pathlib import Path


SCRIPT_PATH = (
    Path(__file__).resolve().parents[1]
    / ".config-sync"
    / "waybar"
    / "scripts"
    / "llm-usage.py"
)


def load_module():
    spec = importlib.util.spec_from_file_location("waybar_llm_usage", SCRIPT_PATH)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    write_bytecode = sys.dont_write_bytecode
    sys.dont_write_bytecode = True
    try:
        spec.loader.exec_module(module)
    finally:
        sys.dont_write_bytecode = write_bytecode
    return module


CODEX_TWO_ACCOUNT_RESPONSE = {
    "version": "1",
    "captured_at": "2026-06-29T06:39:43.911385Z",
    "providers": [
        {
            "provider": "codex",
            "display_name": "Codex",
            "status": "ok",
            "rows": [
                {
                    "identifier": "Codex (5h)",
                    "pct_used": 65,
                    "reset_at": "2026-06-29T10:39:56Z",
                    "is_exhausted": False,
                    "time_until_reset": "in 4h 0m",
                },
                {
                    "identifier": "Codex (7d)",
                    "pct_used": 34,
                    "reset_at": "2026-07-05T23:52:17Z",
                    "is_exhausted": False,
                    "time_until_reset": "in 6d 17h",
                },
                {
                    "identifier": "Codex Spark (5h)",
                    "pct_used": 0,
                    "reset_at": "2026-06-29T11:39:43Z",
                    "is_exhausted": False,
                    "time_until_reset": "in 4h 59m",
                },
                {
                    "identifier": "Codex Spark (7d)",
                    "pct_used": 0,
                    "reset_at": "2026-07-06T06:39:43Z",
                    "is_exhausted": False,
                    "time_until_reset": "in 6d 23h",
                },
            ],
            "availability": [{"name": "Codex", "available_now": True, "available_when": None}],
            "account": "dzackgarza@gmail.com",
            "metadata": {"last_updated": "2026-06-29T06:39:43.793829+00:00"},
            "errors": [],
        },
        {
            "provider": "codex",
            "display_name": "Codex",
            "status": "ok",
            "rows": [
                {
                    "identifier": "Codex (5h)",
                    "pct_used": 1,
                    "reset_at": "2026-06-29T11:39:43Z",
                    "is_exhausted": False,
                    "time_until_reset": "in 4h 59m",
                },
                {
                    "identifier": "Codex (7d)",
                    "pct_used": 0,
                    "reset_at": "2026-07-06T06:39:43Z",
                    "is_exhausted": False,
                    "time_until_reset": "in 6d 23h",
                },
            ],
            "availability": [{"name": "Codex", "available_now": True, "available_when": None}],
            "account": "zack@ncts.ntu.edu.tw",
            "metadata": {"last_updated": "2026-06-29T06:39:43.910829+00:00"},
            "errors": [],
        },
    ],
}


class WaybarLlmUsageTest(unittest.TestCase):
    def test_countdown_formats_reset_as_decimal_hours(self):
        module = load_module()

        self.assertEqual(
            module.countdown(
                "2026-06-29T10:56:00Z",
                now=datetime(2026, 6, 29, 8, 0, tzinfo=timezone.utc),
            ),
            "2.9h",
        )

    def test_codex_payload_displays_each_account_from_usage_limits_contract(self):
        module = load_module()

        payload = module.render_waybar_payload("codex", CODEX_TWO_ACCOUNT_RESPONSE)

        self.assertEqual(
            payload["text"],
            "<span color='#3e4b59'>●</span>"
            "<span color='#aad94c'>65</span>"
            "<span color='#3e4b59'>/</span>"
            "<span color='#aad94c' size='smaller'>34</span>"
            "<span color='#3e4b59'> </span>"
            "<span color='#ffb454'>⚡</span>"
            "<span color='#aad94c'>0</span>"
            "<span color='#3e4b59'>/</span>"
            "<span color='#aad94c' size='smaller'>0</span>"
            "<span color='#3e4b59'> | </span>"
            "<span color='#3e4b59'>●</span>"
            "<span color='#aad94c'>1</span>"
            "<span color='#3e4b59'>/</span>"
            "<span color='#aad94c' size='smaller'>0</span>",
        )
        self.assertEqual(
            payload["tooltip"],
            "Codex - dzackgarza@gmail.com\n"
            "       5h:  65%  resets in 4h 0m\n"
            "       7d:  34%  resets in 6d 17h\n"
            "  Spark 5h:   0%  resets in 4h 59m\n"
            "  Spark 7d:   0%  resets in 6d 23h\n"
            "\n"
            "Codex - zack@ncts.ntu.edu.tw\n"
            "       5h:   1%  resets in 4h 59m\n"
            "       7d:   0%  resets in 6d 23h\n"
            "  Spark 5h:  n/a  resets n/a\n"
            "  Spark 7d:  n/a  resets n/a",
        )
        self.assertEqual(payload["class"], "")

    def test_codex_payload_renders_regular_countdown_and_spark_item_when_exhausted(self):
        module = load_module()
        module.countdown = lambda reset_at: "2.9h"
        data = copy.deepcopy(CODEX_TWO_ACCOUNT_RESPONSE)
        first_account_rows = data["providers"][0]["rows"]
        first_account_rows[0]["pct_used"] = 100
        first_account_rows[0]["is_exhausted"] = True
        first_account_rows[0]["time_until_reset"] = "in 2h 56m"
        first_account_rows[1]["pct_used"] = 43
        first_account_rows[1]["time_until_reset"] = "in 6d 16h"

        payload = module.render_waybar_payload("codex", data)

        self.assertEqual(
            payload["text"],
            "<span color='#3e4b59'>●</span>"
            "<span color='#f07178'>2.9h</span>"
            "<span color='#3e4b59'> </span>"
            "<span color='#ffb454'>⚡</span>"
            "<span color='#aad94c'>0</span>"
            "<span color='#3e4b59'>/</span>"
            "<span color='#aad94c' size='smaller'>0</span>"
            "<span color='#3e4b59'> | </span>"
            "<span color='#3e4b59'>●</span>"
            "<span color='#aad94c'>1</span>"
            "<span color='#3e4b59'>/</span>"
            "<span color='#aad94c' size='smaller'>0</span>",
        )
        self.assertIn("       5h: 100%  resets in 2h 56m", payload["tooltip"])
        self.assertIn("  Spark 5h:   0%  resets in 4h 59m", payload["tooltip"])
        self.assertEqual(payload["class"], "critical")


if __name__ == "__main__":
    unittest.main()
