#!/usr/bin/env bash

set -euo pipefail

for cmd in hyprctl jq rofi; do
    if ! command -v "$cmd" >/dev/null; then
        printf 'Layout: missing %s\n' "$cmd" >&2
        exit 1
    fi
done

definitions="$HOME/.config/hypr/confs/layout-picker.json"
theme="$HOME/.config/rofi/themes/rofi-layout.rasi"
preview_dir="$HOME/.config/hypr/assets/layout-previews"

ws_name="$(hyprctl -j monitors | jq -r '
    first(.[] | select(.focused == true))
    | if (.specialWorkspace.name // "") != ""
      then .specialWorkspace.name
      else .activeWorkspace.name
      end
')"

n="$(hyprctl -j clients | jq --arg ws "$ws_name" '
    [.[] | select(.workspace.name == $ws and (.floating | not) and (.mapped != false))] | length
')"

if (( n == 0 )); then
    notify-send "Layout" "No tiled windows on this workspace"
    exit 0
fi

if ! layout_list="$(jq -r --argjson n "$n" '
    .[]
    | select($n >= .minimum)
    | . as $layout
    | (if $layout.key == "grid"
       then ($n | sqrt | ceil) as $cols
            | ($n / $cols | ceil) as $rows
            | "Grid · \($cols)×\($rows)"
       elif $layout.key == "columns" then "Columns · \($n)"
       elif $layout.key == "rows" then "Rows · \($n)"
       else $layout.label
       end) as $label
    | [$layout.key, $label, $layout.hypr, ($layout.orientation // "")]
    | join("|")
' "$definitions")"; then
    notify-send "Layout" "Could not list layouts"
    exit 1
fi
mapfile -t options <<<"$layout_list"

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
        printf '%s\x00icon\x1f%s\n' "$label" "$preview_dir/$key-$n.png"
    done | rofi -dmenu -i -no-custom -config "$theme" -p "Layout · $n windows"
)" || exit 0

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
