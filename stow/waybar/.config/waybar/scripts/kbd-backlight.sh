#!/bin/bash
DEVICE="platform::kbd_backlight"
MAX=$(brightnessctl -d "$DEVICE" max 2>/dev/null || echo 2)

if [ "$1" = "--toggle" ]; then
    CUR=$(brightnessctl -d "$DEVICE" get 2>/dev/null || echo 0)
    NEXT=$(( (CUR + 1) % (MAX + 1) ))
    brightnessctl -d "$DEVICE" set "$NEXT" -q
fi

CUR=$(brightnessctl -d "$DEVICE" get 2>/dev/null || echo 0)
case "$CUR" in
    0)
        ICON="󰌋"
        CLASS="off"
        TOOLTIP="Keyboard backlight: OFF"
        ;;
    "$MAX")
        ICON="󰌌"
        CLASS="on"
        TOOLTIP="Keyboard backlight: $CUR/$MAX"
        ;;
    *)
        ICON="󰌌"
        CLASS="low"
        TOOLTIP="Keyboard backlight: $CUR/$MAX"
        ;;
esac

echo "{\"text\": \"$ICON\", \"class\": \"$CLASS\", \"tooltip\": \"$TOOLTIP\"}"
