#!/bin/bash
DEVICE="platform::kbd_backlight"
MAX=$(brightnessctl -d "$DEVICE" max 2>/dev/null || echo 2)

if [ "$1" = "--toggle" ]; then
    CUR=$(brightnessctl -d "$DEVICE" get 2>/dev/null || echo 0)
    if [ "$CUR" -gt 0 ]; then
        brightnessctl -d "$DEVICE" set 0 -q
    else
        brightnessctl -d "$DEVICE" set "$MAX" -q
    fi
fi

CUR=$(brightnessctl -d "$DEVICE" get 2>/dev/null || echo 0)
if [ "$CUR" -gt 0 ]; then
    ICON="󰌌"
    CLASS="on"
    TOOLTIP="Keyboard backlight: ON ($CUR/$MAX)"
else
    ICON="󰌋"
    CLASS="off"
    TOOLTIP="Keyboard backlight: OFF"
fi

echo "{\"text\": \"$ICON\", \"class\": \"$CLASS\", \"tooltip\": \"$TOOLTIP\"}"
