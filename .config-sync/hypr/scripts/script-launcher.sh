#!/bin/bash

# Rofi menu
options="Reload Waybar\nSet Random Wallpaper\nSelect Rofi Theme\nCopy Emoji to Clipboard\nChange Waybar Layout\nSelect Lockscreen Style\nEdit Dotfiles\nAdjust Hyprland Settings\nSelect Global Theme\nOpen All PDFs Menu"

choice=$(echo -e "$options" | rofi -dmenu -i -p "Actions")

# Execute command
case "$choice" in
    "Reload Waybar")
        $HOME/.config/hypr/scripts/waybar-reload.sh --reload
        ;;
    "Set Random Wallpaper")
        $HOME/.config/hypr/scripts/Wallpaper.sh
        ;;
    "Select Rofi Theme")
        $HOME/.config/hypr/scripts/rofi_theme.sh
        ;;
    "Copy Emoji to Clipboard")
        $HOME/.config/hypr/scripts/rofi-emoji.sh
        ;;
    "Change Waybar Layout")
        $HOME/.config/hypr/scripts/waybar-layout.sh
        ;;
    "Select Lockscreen Style")
        $HOME/.config/hypr/scripts/hyprlock.sh
        ;;
    "Edit Dotfiles")
        $HOME/.config/hypr/scripts/edit-dotfiles.sh
        ;;
    "Adjust Hyprland Settings")
        $HOME/.config/hypr/scripts/settings.sh
        ;;
    "Select Global Theme")
        $HOME/.config/hypr/scripts/theme_select.sh
        ;;
    "Open All PDFs Menu")
        $HOME/dotfiles/bin/dmenu/dmenuAllPDFs.sh
        ;;
esac