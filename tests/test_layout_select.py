import json
import subprocess
import time
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPT = (
    REPO_ROOT / "stow" / "hypr" / ".config" / "hypr" / "scripts" / "LayoutSelect.sh"
)
ARTIFACT_DIR = Path("/tmp/opencode/layout-select-test")


def layer_namespaces(value):
    namespaces = set()
    if isinstance(value, dict):
        namespace = value.get("namespace")
        if isinstance(namespace, str):
            namespaces.add(namespace)
        for child in value.values():
            namespaces.update(layer_namespaces(child))
    elif isinstance(value, list):
        for child in value:
            namespaces.update(layer_namespaces(child))
    return namespaces


class LayoutSelectTest(unittest.TestCase):
    def setUp(self):
        ARTIFACT_DIR.mkdir(parents=True, exist_ok=True)
        output = subprocess.check_output(["hyprctl", "-j", "layers"], text=True)
        self.assertNotIn("rofi", layer_namespaces(json.loads(output)))

    def rofi_visible(self):
        output = subprocess.check_output(["hyprctl", "-j", "layers"], text=True)
        return "rofi" in layer_namespaces(json.loads(output))

    def cancel(self, process):
        if self.rofi_visible():
            subprocess.run(["wtype", "-k", "Escape"], check=True)
        if process.poll() is None:
            process.kill()
        stdout, stderr = process.communicate()
        (ARTIFACT_DIR / "cancel-stdout.log").write_text(stdout)
        (ARTIFACT_DIR / "cancel-stderr.log").write_text(stderr)

    def test_real_picker_appears_without_launcher_startup_delay(self):
        start = time.perf_counter()
        process = subprocess.Popen(
            [SCRIPT],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
        self.addCleanup(self.cancel, process)

        while (
            not self.rofi_visible()
            and process.poll() is None
            and time.perf_counter() - start < 10
        ):
            time.sleep(0.01)
        elapsed = time.perf_counter() - start

        if not self.rofi_visible():
            stdout, stderr = process.communicate()
            evidence = {
                "mapped": False,
                "seconds": elapsed,
                "returncode": process.returncode,
                "stdout": stdout,
                "stderr": stderr,
            }
            (ARTIFACT_DIR / "evidence.json").write_text(
                json.dumps(evidence, indent=2) + "\n"
            )
            self.fail(f"Rofi did not appear: {evidence}")

        subprocess.run(["grim", str(ARTIFACT_DIR / "layout-picker.png")], check=True)
        subprocess.run(["wtype", "-k", "Escape"], check=True)
        stdout, stderr = process.communicate(timeout=10)
        evidence = {
            "mapped": True,
            "seconds": elapsed,
            "returncode": process.returncode,
            "stdout": stdout,
            "stderr": stderr,
        }
        (ARTIFACT_DIR / "evidence.json").write_text(
            json.dumps(evidence, indent=2) + "\n"
        )

        self.assertEqual(process.returncode, 0, evidence)
        self.assertLess(elapsed, 1.0, evidence)


if __name__ == "__main__":
    unittest.main()
