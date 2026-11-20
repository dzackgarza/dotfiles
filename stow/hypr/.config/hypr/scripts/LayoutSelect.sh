#!/usr/bin/env bash

set -euo pipefail

scripts_dir="$HOME/.config/hypr/scripts"
theme="$HOME/.config/rofi/themes/rofi-layout.rasi"
cache_dir="${XDG_CACHE_HOME:-$HOME/.cache}/hypr/layout-previews"

ws_json="$(hyprctl -j activeworkspace)"
ws_name="$(hyprctl -j monitors | jq -r 'first(.[] | select(.focused == true)) // {} | .specialWorkspace.name // ""')"
if [[ -z "$ws_name" ]]; then
    ws_name="$(jq -r '.name' <<<"$ws_json")"
fi

n="$(hyprctl -j clients | jq --arg ws "$ws_name" '
    [.[] | select(.workspace.name == $ws and (.floating | not) and (.mapped != false))] | length
')"

if (( n == 0 )); then
    notify-send "Layout" "No tiled windows on this workspace"
    exit 0
fi

if ! layout_list="$(python3 "$scripts_dir/generate-layout-previews.py" --list --count "$n")"; then
    notify-send "Layout" "Could not list layouts"
    exit 1
fi
mapfile -t options <<<"$layout_list"

if ! python3 "$scripts_dir/generate-layout-previews.py" --count "$n" --out "$cache_dir"; then
    notify-send "Layout" "Could not build layout previews"
    exit 1
fi

# Each line is `key|label|hypr-layout|orientation`.
declare -A key_by_label=()
declare -A hypr_by_key=()
declare -A orientation_by_key=()
for line in "${options[@]}"; do
    IFS='|' read -r key label hypr orientation <<<"$line"
    key_by_label["$label"]="$key"
    hypr_by_key["$key"]="$hypr"
    orientation_by_key["$key"]="$orientation"
done

choice="$(
    for line in "${options[@]}"; do
        IFS='|' read -r key label _ _ <<<"$line"
        printf '%s\x00icon\x1f%s\n' "$label" "$cache_dir/$key-$n.png"
    done | rofi -dmenu -i -no-custom -config "$theme" -p "Layout · $n windows"
)"

[[ -z "$choice" ]] && exit 0

key="${key_by_label[$choice]:-}"
[[ -z "$key" ]] && exit 0

layout="${hypr_by_key[$key]:-}"
if [[ -z "$layout" ]]; then
    notify-send "Layout" "Unknown layout: $key"
    exit 1
fi

orientation="${orientation_by_key[$key]:-}"
opts=""
if [[ -n "$orientation" ]]; then
    opts=", layout_opts = { orientation = \"$orientation\" }"
fi

ws_lua="$(jq -Rn --arg ws "$ws_name" '$ws')"

if ! hyprctl eval "hl.workspace_rule({ workspace = $ws_lua, layout = \"$layout\"$opts })" >/dev/null; then
    notify-send "Layout" "Could not apply $key"
    exit 1
fi
