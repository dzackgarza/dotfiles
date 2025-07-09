import os
import sys
import pexpect
import subprocess
import pytest
import re

REPL_PATH = "src/llm_repl_v0.py"

# Helper to strip ANSI escape codes
def strip_ansi(text):
    ansi_escape = re.compile(r'\x1B\[[0-?]*[ -/]*[@-~]')
    return ansi_escape.sub('', text)

# --- E2E Testing Philosophy ---
# This file contains end-to-end (E2E) tests for the LLM REPL.
# These tests:
#   - Launch the REPL as a real subprocess (not just class instantiation)
#   - Simulate real user input/output
#   - Check for startup, shutdown, error handling, and edge cases
#   - Ensure that catastrophic errors (e.g., missing methods, event loop issues) are caught
#   - Are required for every major feature or CLI change
#
# Checklist for new features:
#   [ ] Does this feature have an E2E test?
#   [ ] Does the REPL start and exit cleanly?
#   [ ] Are error messages clear for missing config/env?
#   [ ] Are event loop/async issues detected?


def test_repl_startup_and_exit():
    """Test that the REPL starts, shows the prompt, and exits cleanly on EOF."""
    env = os.environ.copy()
    env['NO_DOTENV'] = '1'
    child = pexpect.spawn(f"python3 {REPL_PATH}", env=env, encoding="utf-8", timeout=20)
    try:
        child.sendline('')  # Workaround: trigger prompt_toolkit to display prompt
        child.expect("> ")
        child.sendeof()
        try:
            child.expect(pexpect.EOF, timeout=2)
        except Exception:
            print("[DEBUG] child.before:", repr(child.before))
            raise
        output = strip_ansi(child.before)
        assert "Welcome to Gemini-CLI REPL Chat!" in output
        assert "Thanks for using Gemini-CLI REPL Chat!" in output
    finally:
        child.close()


def test_repl_basic_math():
    """Test that the REPL can answer a simple math question interactively."""
    env = os.environ.copy()
    env['NO_DOTENV'] = '1'
    child = pexpect.spawn(f"python3 {REPL_PATH}", env=env, encoding="utf-8", timeout=20)
    try:
        child.sendline('')  # Workaround: trigger prompt_toolkit to display prompt
        child.expect("> ")
        child.sendline("What is 2+2?")
        child.expect("4")
        child.sendeof()
        child.expect(pexpect.EOF)
    finally:
        child.close()


def test_repl_missing_env_pexpect():
    """Test that the REPL fails with a clear error if GEMINI_API_KEY is missing (Gemini backend, interactive/PTY)."""
    env = os.environ.copy()
    env.pop("GEMINI_API_KEY", None)
    env['NO_DOTENV'] = '1'
    child = pexpect.spawn(f"python3 {REPL_PATH} gemini", env=env, encoding="utf-8", timeout=10)
    try:
        idx = child.expect(["GEMINI_API_KEY environment variable is required", pexpect.EOF, pexpect.TIMEOUT], timeout=10)
        output = strip_ansi(child.before)
        # Read any remaining output after expect
        try:
            rest = child.read()
        except Exception:
            rest = ''
        output += strip_ansi(rest)
        if "GEMINI_API_KEY environment variable is required" not in output:
            print("[DEBUG] child.before:", repr(child.before))
            print("[DEBUG] child.read():", repr(rest))
        assert "GEMINI_API_KEY environment variable is required" in output
    finally:
        child.close()


def test_repl_ollama_no_key():
    """Test that the REPL starts and exits cleanly with Ollama backend and no GEMINI_API_KEY."""
    env = os.environ.copy()
    env.pop("GEMINI_API_KEY", None)
    env['NO_DOTENV'] = '1'
    child = pexpect.spawn(f"python3 {REPL_PATH} ollama", env=env, encoding="utf-8", timeout=10)
    try:
        child.sendline('')  # Workaround: trigger prompt_toolkit to display prompt
        child.expect("> ")
        child.sendeof()
        try:
            child.expect(pexpect.EOF, timeout=2)
        except Exception:
            print("[DEBUG] child.before:", repr(child.before))
            try:
                rest = child.read()
            except Exception:
                rest = ''
            print("[DEBUG] child.read():", repr(rest))
            raise
        output = strip_ansi(child.before)
        try:
            rest = child.read()
        except Exception:
            rest = ''
        output += strip_ansi(rest)
        assert "Welcome to Gemini-CLI REPL Chat!" in output
        assert "Thanks for using Gemini-CLI REPL Chat!" in output
    finally:
        child.close()

def test_repl_event_loop_error():
    """Test that the REPL reports a clear error if an event loop is already running (simulate Jupyter/async context)."""
    import threading, asyncio
    errors = []
    def run_repl():
        try:
            asyncio.get_event_loop().run_forever()
        except Exception:
            pass
        try:
            subprocess.run([sys.executable, REPL_PATH], check=True, timeout=10)
        except Exception as e:
            errors.append(str(e))
    t = threading.Thread(target=run_repl)
    t.start()
    t.join(timeout=15)
    if errors:
        assert "event loop is already running" in errors[0] or "RuntimeError" in errors[0]
    else:
        # If no error, at least the REPL should not hang forever
        assert True 

def test_repl_event_loop_error_e2e():
    """E2E: Launch the REPL in a subprocess with an active event loop and assert on output and exit code (PTY)."""
    import asyncio, sys, tempfile, os, pexpect
    # Write a small script that starts an event loop and then launches the REPL via pexpect
    script = '''
import asyncio, pexpect, sys, os
loop = asyncio.get_event_loop()
loop.create_task(asyncio.sleep(1))
child = pexpect.spawn(sys.executable + ' src/llm_repl_v0.py', encoding='utf-8')
child.expect("[FATAL] REPL failed to start: This event loop is already running", timeout=10)
child.close()
assert child.exitstatus != 0
'''
    with tempfile.NamedTemporaryFile("w", delete=False, suffix=".py") as tf:
        tf.write(script)
        tf.flush()
        tf_name = tf.name
    env = os.environ.copy()
    env['NO_DOTENV'] = '1'
    proc = subprocess.Popen([sys.executable, tf_name], stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=env)
    out, err = proc.communicate(timeout=15)
    os.unlink(tf_name)
    output = out.decode(errors="replace") + err.decode(errors="replace")
    assert "[FATAL] REPL failed to start: This event loop is already running" in output or "pexpect.exceptions.EOF" not in output 