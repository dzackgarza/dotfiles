# Control Center Integration TODO

## Goal
Hook every mock tile in `mybar.tsx` to real system state/actions, with no placeholder data.

## Implementation rules
- Build one data/action layer (e.g. `services/control-center.ts`) and bind UI to that.
- Reuse existing scripts in `~/.config/hypr/scripts` where they already exist.
- If a dependency is missing (e.g. `swaync-client`, `brightnessctl`), fail visibly in the tile state.

## Tile-by-tile plan

### Connectivity + modes
- [ ] **Bluetooth tile**
  - Read: adapter powered state + connected device count (Astal Bluetooth).
  - Toggle: adapter powered on/off.
  - UI: active highlight when powered on.
- [ ] **Wi-Fi tile**
  - Read: enabled state, SSID, signal strength (Astal Network / NM).
  - Toggle: wifi radio on/off.
  - UI lines: `Connected/Disconnected • bars` + SSID.
- [ ] **Power profile tile**
  - Read: active profile from power-profiles-daemon.
  - Action: set `power-saver`, `balanced`, `performance`.
  - Icons: leaf / scale / bolt.
- [ ] **Appearance tile**
  - Read: current mode from `gsettings get org.gnome.desktop.interface color-scheme`.
  - Toggle: dark/light via `gsettings set ...`.
- [ ] **Silent tile**
  - Read: DND state from `swaync-client`.
  - Toggle: `swaync-client -d -sw`.
- [ ] **Mic mute tile**
  - Read + toggle using existing `~/.config/hypr/scripts/volumecontrol.sh --toggle-mic`.

### Info + usage
- [ ] **CPU tile**
  - Read: real CPU % + frequency + core count from `/proc` (poll).
- [ ] **Memory tile**
  - Read: used/total RAM + swap from `/proc/meminfo`.
- [ ] **Disk tile**
  - Read: filesystem usage from `df`/`statvfs` for `/` and `/home`.
- [ ] **AI usage tile**
  - Read: `~/.config/hypr/claude_usage_data.json` (5h/7d utilization + reset times).
  - Optional: add summary stats file for sessions/messages/tokens if available.
- [ ] **Updates tile**
  - Read package count using `~/.config/hypr/scripts/systemupdate.sh --check` (JSON parse).
  - Secondary line: last successful check timestamp formatted like `Wed. Feb 04, 19:20`.
- [ ] **Notification center tile**
  - Read unread count + latest preview from `swaync-client`.
  - Action: open center (`swaync-client -t -sw`).

### Sliders + bottom status
- [ ] **Volume slider**
  - Read/write default sink volume (PipeWire/WirePlumber via Astal WP or existing volume script).
- [ ] **Brightness slider**
  - Read/write brightness via `~/.config/hypr/scripts/brightness.sh` (or direct `brightnessctl`).
- [ ] **Battery status block**
  - Read: percent, remaining time, wattage from UPower (`org.freedesktop.UPower`).
  - Keep 3 consistent rows with icons (battery-bolt, hourglass, wattage).
- [ ] **Power buttons**
  - Suspend: `systemctl suspend`
  - Hibernate: `systemctl hibernate`
  - Power off: `~/.config/hypr/scripts/power.sh --poweroff`

## Window behavior + UX
- [ ] Keep current outside-click catcher and Escape-to-close behavior on both panel + catcher windows.
- [ ] Add `last updated` timestamp sourced from real poll updates, not static strings.
- [ ] Add visible error state per tile when its backend command/service fails.

## Verification checklist
- [ ] Each toggle changes real system state.
- [ ] Every displayed number/label updates from live data.
- [ ] Waybar button opens/closes panel cleanly (`ags toggle claude-usage`).
- [ ] Outside click and Escape close the panel reliably.
