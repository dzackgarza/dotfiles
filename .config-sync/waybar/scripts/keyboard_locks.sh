#!/bin/bash

# Script to show keyboard lock status (capslock, numlock) for Waybar using hyprctl

# Function to get keyboard state using hyprctl
get_keyboard_state() {
    # Get the full hyprctl devices output
    devices_output=$(hyprctl devices 2>/dev/null)
    
    # Find the main keyboard section
    # First, find the line with main: yes and extract the preceding keyboard info
    main_keyboard_start=$(echo "$devices_output" | grep -n "main: yes" | head -n1 | cut -d: -f1)
    
    # Get the starting line of the main keyboard (go back to find the Keyboard line)
    keyboard_info_start=$(echo "$devices_output" | head -n "$main_keyboard_start" | grep -n "Keyboard at" | tail -n1 | cut -d: -f1)
    
    # Extract the relevant section for the main keyboard
    main_keyboard_section=$(echo "$devices_output" | sed -n "${keyboard_info_start},$(echo "$main_keyboard_start" | awk '{print $1+3}')p")
    
    # Extract capslock status from main keyboard
    if echo "$main_keyboard_section" | grep -q "capsLock: yes"; then
        caps_status="C:🟢"  # Green circle for ON
    else
        caps_status="C:🔴"  # Red circle for OFF
    fi
    
    # Extract numlock status from main keyboard
    if echo "$main_keyboard_section" | grep -q "numLock: yes"; then
        num_status=" #:🟢 "  # Green circle for ON
    else
        num_status=" #:🔴 "  # Red circle for OFF
    fi
    
    echo -n "$caps_status$num_status"
}

# For Waybar custom module, output JSON once and exit
# Waybar will run the script at the specified interval
output=$(get_keyboard_state)
echo "{\"text\": \"$output\", \"tooltip\": \"Keyboard Lock Status\"}"
