#!/usr/bin/env python3

import json
import os
import shutil
import subprocess
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path


def state_path():
    """Return the shared package-update snapshot path."""
    state_home = Path(
        os.environ.get("XDG_STATE_HOME", str(Path.home() / ".local" / "state"))
    )
    return state_home / "ags" / "package-updates.json"


def read_state():
    """Read the last timer-maintained snapshot without running a package tool."""
    path = state_path()
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        return {"text": "?", "tooltip": "Update status has not been checked yet"}
    except json.JSONDecodeError:
        return {"text": "?", "tooltip": "Update status file is invalid"}


def write_state(result):
    """Atomically publish a package-update snapshot for desktop consumers."""
    path = state_path()
    path.parent.mkdir(parents=True, exist_ok=True)
    snapshot = {
        **result,
        "checked_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
    }
    temporary_path = None
    try:
        with tempfile.NamedTemporaryFile(
            mode="w",
            encoding="utf-8",
            dir=path.parent,
            prefix=f".{path.name}.",
            delete=False,
        ) as temporary:
            json.dump(snapshot, temporary, ensure_ascii=False)
            temporary.write("\n")
            temporary.flush()
            os.fsync(temporary.fileno())
            temporary_path = Path(temporary.name)
        os.replace(temporary_path, path)
    finally:
        if temporary_path is not None and temporary_path.exists():
            temporary_path.unlink()
    return snapshot


def ping_test():
    """Test if we have internet connectivity."""
    result = subprocess.run(
        ["ping", "-c", "1", "-W", "1", "google.com"],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )
    return result.returncode == 0


def get_pacman_updates():
    """Get updates for pacman-based systems with download size info."""
    aurhlpr = shutil.which("paru") or shutil.which("yay")
    if not aurhlpr:
        return 0, 0, False

    # Get AUR updates count
    aur_result = subprocess.run([aurhlpr, "-Qua"], capture_output=True, text=True)
    aur_updates = len([line for line in aur_result.stdout.split('\n') if line.strip() and 'ignored' not in line.lower()]) if aur_result.returncode == 0 else 0

    # Get pacman updates count and package names in a single run
    pacman_result = subprocess.run(["checkupdates"], capture_output=True, text=True)
    pacman_lines = [line.strip() for line in pacman_result.stdout.split('\n') if line.strip()] if pacman_result.returncode == 0 else []
    pacman_updates = len(pacman_lines)
    
    total_updates = aur_updates + pacman_updates
    download_size = 0.0
    
    if total_updates > 0 and pacman_lines:
        packages = [line.split()[0] for line in pacman_lines]

        # Query all package details at once instead of in a loop
        size_result = subprocess.run(
            ["pacman", "-Si"] + packages,
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
            text=True
        )
        
        total_size = 0.0
        for line in size_result.stdout.split('\n'):
            if 'installed size' in line.lower():
                # Format: "Installed Size  : 123.45 MiB"
                parts = line.split(':', 1)
                if len(parts) > 1:
                    value_str = parts[1].strip().split()
                    if len(value_str) >= 2:
                        try:
                            size_value = float(value_str[0])
                            unit = value_str[1].lower()
                            if 'kib' in unit:
                                size_value /= 1024
                            elif 'b' in unit and 'mib' not in unit:
                                size_value /= 1024 * 1024
                            total_size += size_value
                        except ValueError:
                            continue
        download_size = round(total_size, 2)
    
    has_downloaded = False
    return total_updates, download_size, has_downloaded


def get_dnf_updates():
    """Get updates for dnf-based systems."""
    result = subprocess.run(["dnf", "check-update", "-q"], capture_output=True, text=True)
    updates = [line for line in result.stdout.splitlines() if line.strip()]
    return len(updates), 0.0


def get_zypper_updates():
    """Get updates for zypper-based systems."""
    result = subprocess.run(["zypper", "lu", "--best-effort"], capture_output=True, text=True)
    count = sum(1 for line in result.stdout.splitlines() if 'v  |' in line)
    return count, 0.0


def query_updates():
    """Query available updates; callers decide whether to publish the result."""
    if not ping_test():
        return {"text": "?", "tooltip": "Network not available"}
    
    # Check for pacman-based systems
    if shutil.which("pacman"):
        updates, download_size, _ = get_pacman_updates()
        
        if updates > 0:
            # Always show (!) to indicate updates are available to be installed
            display_text = f"{updates} (!)"
            tooltip = f"󱓽 Updates Available: {updates} ({download_size:.2f} MiB)\n\nPress CTRL + U to update"
            result = {"text": display_text, "tooltip": tooltip}
        else:
            result = {"text": "✓", "tooltip": "  Packages are up to date"}
        
        return result
    
    # Check for dnf-based systems
    elif shutil.which("dnf"):
        updates, _ = get_dnf_updates()
        
        if updates > 0:
            display_text = f"{updates} (!)"  # DNF typically needs to download
            tooltip = f"󱓽 Updates Available: {updates}\n\npress ctrl + u to update"
            result = {"text": display_text, "tooltip": tooltip}
        else:
            result = {"text": "✓", "tooltip": "  Packages are up to date"}
        
        return result
    
    # Check for zypper-based systems
    elif shutil.which("zypper"):
        updates, _ = get_zypper_updates()
        
        if updates > 0:
            display_text = f"{updates} (!)"  # Zypper typically needs to download
            tooltip = f"󱓽 Updates Available: {updates}\n\nPress CTRL + U to update"
            result = {"text": display_text, "tooltip": tooltip}
        else:
            result = {"text": "✓", "tooltip": "  Packages are up to date"}
        
        return result

    return {"text": "?", "tooltip": "No supported package manager found"}


def package_update():
    """Perform package update."""
    scripts_dir = Path(__file__).parent
    waybar_reload_script = scripts_dir / "waybar-reload.sh"

    # Update for pacman-based systems
    if shutil.which("pacman"):
        aurhlpr = shutil.which("paru") or shutil.which("yay") or "yay"
        subprocess.run(["kitty", "--title", "update", "sh", "-c", f"{aurhlpr} -Syu"])

    # Update for dnf-based systems
    elif shutil.which("dnf"):
        subprocess.run(["kitty", "--title", "update", "sh", "-c", "sudo dnf upgrade"])

    # Update for zypper-based systems
    elif shutil.which("zypper"):
        subprocess.run(["kitty", "--title", "update", "sh", "-c", "sudo zypper dup"])

    # Reload waybar (if the script exists)
    if waybar_reload_script.exists():
        subprocess.run([str(waybar_reload_script), "--reload"])


def main():
    if len(sys.argv) < 2:
        print("Usage: python systemupdate.py --check|--refresh|--update")
        sys.exit(1)
    
    if sys.argv[1] == "--check":
        print(json.dumps(read_state(), ensure_ascii=False))
    elif sys.argv[1] == "--refresh":
        print(json.dumps(write_state(query_updates()), ensure_ascii=False))
    elif sys.argv[1] == "--update":
        package_update()
    else:
        print("Invalid option. Use '--check', '--refresh', or '--update'.")
        sys.exit(1)


if __name__ == "__main__":
    main()
