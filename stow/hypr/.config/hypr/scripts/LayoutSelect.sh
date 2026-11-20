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

mapfile -t options < <(python3 "$scripts_dir/generate-layout-previews.py" --list --count "$n")

missing=0
for line in "${options[@]}"; do
    key="${line%%|*}"
    [[ -f "$cache_dir/$key-$n.png" ]] || missing=1
done

if (( missing )); then
    python3 "$scripts_dir/generate-layout-previews.py" --count "$n" --out "$cache_dir"
fi

declare -A key_by_label=()
for line in "${options[@]}"; do
    key="${line%%|*}"
    label="${line#*|}"
    key_by_label["$label"]="$key"
done

choice="$(
    for line in "${options[@]}"; do
        key="${line%%|*}"
        label="${line#*|}"
        printf '%s\x00icon\x1f%s\n' "$label" "$cache_dir/$key-$n.png"
    done | rofi -dmenu -i -no-custom -config "$theme" -p "Layout · $n windows"
)"

[[ -z "$choice" ]] && exit 0

key="${key_by_label[$choice]:-}"
[[ -z "$key" ]] && exit 0

ws_lua="$(jq -Rn --arg ws "$ws_name" '$ws')"

case "$key" in
    dwindle | monocle)
        layout="$key"
        opts=""
        ;;
    master-left | master-right | master-top | master-bottom | master-center)
        layout="master"
        opts=", layout_opts = { orientation = \"${key#master-}\" }"
        ;;
    grid | columns | rows | center)
        layout="lua:$key"
        opts=""
        ;;
    *)
        notify-send "Layout" "Unknown layout: $key"
        exit 1
        ;;
esac

if ! hyprctl eval "hl.workspace_rule({ workspace = $ws_lua, layout = \"$layout\"$opts })" >/dev/null; then
    notify-send "Layout" "Could not apply $key"
    exit 1
fi
