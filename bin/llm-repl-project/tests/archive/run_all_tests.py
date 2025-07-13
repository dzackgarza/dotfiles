import subprocess
import sys
import os

tests = [
    "test_code_and_numeric",
    "test_table_rendering",
    "test_latex_rendering",
    "test_multiline_input",
    "test_command_autocompletion",
    "test_streaming_response",
    "test_historydb_persistence_and_search",
    "test_session_management",
]

all_passed = True
failed_tests = []
for test in tests:
    print(f"Running {test}...")
    env = os.environ.copy()
    env["PYTHONUNBUFFERED"] = "1"
    result = subprocess.run(["/usr/bin/python3", "tests/test_llm_repl.py", test], text=True, env=env)
    print("[DEBUG] result:", result)
    if result.returncode != 0:
        print(f"[FAIL] {test} failed with exit code {result.returncode}")
        failed_tests.append(test)
        all_passed = False
    else:
        print(f"[PASS] {test}")

if all_passed:
    print("[ALL PASS] All tests passed.")
    sys.exit(0)
else:
    print(f"[FAIL] {len(failed_tests)} test(s) failed: {', '.join(failed_tests)}")
    sys.exit(1) 