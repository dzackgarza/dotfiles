#!/bin/bash

case $1 in
    --poweroff)
        "$HOME/.config/hypr/scripts/uptime.sh"
        "$HOME/.config/hypr/scripts/notification.sh" logout
        systemctl poweroff --now
        ;;
    --reboot)
        "$HOME/.config/hypr/scripts/uptime.sh"
        "$HOME/.config/hypr/scripts/notification.sh" logout
        systemctl reboot --now
        ;;
    --logout)
        "$HOME/.config/hypr/scripts/uptime.sh"
        "$HOME/.config/hypr/scripts/notification.sh" logout
        hyprctl eval 'hl.dispatch(hl.dsp.exit())'
        ;;
    --lock)
        hyprlock
        ;;
esac
