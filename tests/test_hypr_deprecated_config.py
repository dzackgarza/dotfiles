import json
import subprocess
import unittest


class HyprDeprecatedConfigTest(unittest.TestCase):
    def test_running_config_has_no_deprecated_options(self):
        output = subprocess.check_output(
            ["hyprctl", "-j", "deprecated-config"], text=True
        )
        self.assertEqual(json.loads(output), [])


if __name__ == "__main__":
    unittest.main()
