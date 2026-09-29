#!/usr/bin/env bash

set -euo pipefail

theme="$HOME/.config/rofi/themes/rofi-keybinds.rasi"
export XDG_RUNTIME_DIR="${XDG_RUNTIME_DIR:-/run/user/$(id -u)}"
export DISPLAY="${DISPLAY:-:0}"

if [[ -z "${HYPRLAND_INSTANCE_SIGNATURE:-}" ]]; then
    HYPRLAND_INSTANCE_SIGNATURE="$(hyprctl instances | awk '/^instance/{gsub(":", "", $2); print $2; exit}')"
    export HYPRLAND_INSTANCE_SIGNATURE
fi

if ! command -v hyprctl >/dev/null || ! command -v jq >/dev/null || ! command -v rofi >/dev/null; then
    notify-send "Keybinds" "hyprctl, jq, and rofi are required"
    exit 1
fi

bind_json="$({
    hyprctl -j binds
} 2>/dev/null)" || {
    notify-send "Keybinds" "Could not read registered Hyprland bindings"
    exit 1
}

binds="$(printf '%s' "$bind_json" | jq -r '
    def modifier($mask; $bit; $name):
        if (($mask / $bit | floor) % 2) == 1 then [$name] else [] end;
    def key_name:
        if . == "Return" then "Enter"
        elif . == "Space" then "Space"
        elif . == "escape" then "Esc"
        elif . == "print" then "Print"
        else .
        end;
    .[]
    | ((modifier(.modmask; 64; "SUPER")
        + modifier(.modmask; 8; "ALT")
        + modifier(.modmask; 4; "CTRL")
        + modifier(.modmask; 1; "SHIFT")) | join(" + ")) as $mods
    | (($mods + (if $mods == "" then "" else " + " end) + (.key | key_name))) as $keys
    | (if .submap == "" or .submap == "_ROOT" then "" else "[" + .submap + "] " end) as $scope
    | (if .has_description then .description
       elif .arg == "" then .dispatcher
       else .dispatcher + " " + .arg
       end) as $action
    | $scope + $keys + "  —  " + $action
')" || {
    notify-send "Keybinds" "Could not read registered Hyprland bindings"
    exit 1
}

if [[ -z "$binds" ]]; then
    notify-send "Keybinds" "No registered bindings"
    exit 1
fi

selected_index="$(printf '%s\n' "$binds" | rofi -dmenu -i -no-custom -format i -p "Keybinds" -theme "$theme")"
[[ -z "$selected_index" ]] && exit 0
[[ "$selected_index" =~ ^[0-9]+$ ]] || {
    notify-send "Keybinds" "Could not identify selected binding"
    exit 1
}

request="$(printf '%s' "$bind_json" | jq -r --argjson index "$selected_index" '
    def modifier($mask; $bit; $name):
        if (($mask / $bit | floor) % 2) == 1 then [$name] else [] end;
    .[$index]
    | ((modifier(.modmask; 64; "SUPER")
        + modifier(.modmask; 8; "ALT")
        + modifier(.modmask; 4; "CTRL")
        + modifier(.modmask; 1; "SHIFT")) | join(" + ")) as $mods
    | "hypr_keybind_run("
      + (($mods + (if $mods == "" then "" else " + " end) + .key) | @json)
      + ","
      + ((if .has_description then .description else "" end) | @json)
      + ","
      + ((.submap // "") | @json)
      + ")"
')" || {
    notify-send "Keybinds" "Could not identify selected binding"
    exit 1
}

hyprctl eval "$request" >/dev/null 2>&1 || {
    notify-send "Keybinds" "Could not run selected keybind"
    exit 1
}
