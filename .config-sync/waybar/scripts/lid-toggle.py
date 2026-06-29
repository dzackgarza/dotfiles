#!/usr/bin/env python3
"""Waybar custom module for toggling lid-close behavior."""

import json
import os
import signal
import subprocess
import sys
import time
from pathlib import Path


SYSTEMD_ANALYZE = Path("/usr/bin/systemd-analyze")
SYSTEMD_INHIBIT = Path("/usr/bin/systemd-inhibit")
SLEEP = Path("/usr/bin/sleep")
WHO = "waybar-lid-toggle"
WHY = "Waybar lid toggle: ignore lid close"
WHAT = "handle-lid-switch"


def _assert_setup() -> None:
    for binary in (SYSTEMD_ANALYZE, SYSTEMD_INHIBIT, SLEEP):
        assert binary.is_file(), f"required systemd lid-toggle binary missing: {binary}"
    runtime_dir = os.environ.get("XDG_RUNTIME_DIR")
    assert runtime_dir, "XDG_RUNTIME_DIR is required for the Waybar lid-toggle pidfile"
    assert Path(runtime_dir).is_dir(), f"XDG_RUNTIME_DIR does not exist: {runtime_dir}"


def _state_dir() -> Path:
    runtime_dir = Path(os.environ["XDG_RUNTIME_DIR"])
    state_dir = runtime_dir / "waybar-lid-toggle"
    state_dir.mkdir(mode=0o700, exist_ok=True)
    return state_dir


def _pidfile() -> Path:
    return _state_dir() / "inhibitor.pid"


def _cmdline(pid: int) -> list[str] | None:
    proc_cmdline = Path("/proc") / str(pid) / "cmdline"
    if not proc_cmdline.exists():
        return None
    parts = proc_cmdline.read_bytes().split(b"\0")
    return [part.decode() for part in parts if part]


def _managed_pid() -> int | None:
    pidfile = _pidfile()
    if not pidfile.exists():
        return None
    pid_text = pidfile.read_text().strip()
    assert pid_text.isdecimal(), f"invalid lid-toggle pidfile contents: path={pidfile} value={pid_text!r}"
    pid = int(pid_text)
    cmdline = _cmdline(pid)
    if cmdline is None:
        pidfile.unlink()
        return None
    assert WHO in " ".join(cmdline) and WHAT in " ".join(cmdline), (
        f"lid-toggle pidfile points at an unexpected process: pid={pid} cmdline={cmdline}; "
        f"remove {pidfile} after inspecting the process"
    )
    return pid


def _logind_lid_action() -> str:
    merged = subprocess.check_output(
        [SYSTEMD_ANALYZE, "cat-config", "systemd/logind.conf"],
        text=True,
    )
    action = ""
    for line in merged.splitlines():
        stripped = line.strip()
        if stripped.startswith("HandleLidSwitch="):
            action = stripped.split("=", 1)[1]
    assert action, "HandleLidSwitch is not explicitly configured in systemd/logind.conf"
    return action


def _stop_inhibitor() -> None:
    pid = _managed_pid()
    if pid is None:
        return
    os.kill(pid, signal.SIGTERM)
    for _ in range(20):
        if _cmdline(pid) is None:
            _pidfile().unlink(missing_ok=True)
            return
        time.sleep(0.05)
    os.kill(pid, signal.SIGKILL)
    _pidfile().unlink(missing_ok=True)


def _start_inhibitor() -> None:
    assert _managed_pid() is None, "lid-close ignore inhibitor is already active"
    process = subprocess.Popen(
        [
            SYSTEMD_INHIBIT,
            f"--what={WHAT}",
            "--mode=block",
            f"--who={WHO}",
            f"--why={WHY}",
            SLEEP,
            "infinity",
        ],
        stdin=subprocess.DEVNULL,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        start_new_session=True,
    )
    _pidfile().write_text(f"{process.pid}\n")


def _mode() -> str:
    return "ignore" if _managed_pid() is not None else _logind_lid_action()


def _payload(mode: str) -> dict[str, str]:
    next_mode = "hibernate" if mode == "ignore" else "ignore"
    return {
        "text": f"lid:{mode}",
        "tooltip": f"Lid close action: {mode}\nClick to switch to {next_mode}",
        "class": mode,
    }


def _set_mode(mode: str) -> dict[str, str]:
    assert mode in {"hibernate", "ignore"}, f"unsupported lid-toggle mode: {mode}"
    if mode == "ignore":
        _start_inhibitor()
    else:
        _stop_inhibitor()
    return _payload(_mode())


def main() -> None:
    _assert_setup()
    args = sys.argv[1:]
    if args == [] or args == ["--status"]:
        payload = _payload(_mode())
    elif args == ["--toggle"]:
        payload = _set_mode("hibernate" if _mode() == "ignore" else "ignore")
    elif len(args) == 2 and args[0] == "--set":
        payload = _set_mode(args[1])
    else:
        raise AssertionError(f"usage: {Path(sys.argv[0]).name} [--status|--toggle|--set hibernate|--set ignore]")
    print(json.dumps(payload))


if __name__ == "__main__":
    main()
