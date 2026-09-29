#!/bin/bash

iDIR="$HOME/.config/hypr/icons/vol"

# Get Volume
get_volume() {
    volume=$(pactl get-sink-volume @DEFAULT_SINK@ | grep -oP '\d+%' | head -1 | tr -d '%')
    if [[ "$volume" -eq "0" ]]; then
        echo "Muted"
    else
        echo "${volume}%"
    fi
}

# Get icons
get_icon() {
    current=$(get_volume)
    if [[ "$current" == "Muted" ]]; then
        echo "$iDIR/muted-speaker.svg"
    else
        echo "$iDIR/vol-${current%\%}.svg"
    fi
}

# Notify using dunst
# notify_user() {
#     if [[ "$(get_volume)" == " " ]]; then
#         notify-send -a -r -h string:x-dunst-stack-tag:volume_notif -i "$(get_icon)" "Volume: Muted"
#     else
#         notify-send -a -r -h string:x-dunst-stack-tag:volume_notif -i "$(get_icon)" "Volume: $(get_volume)"
#     fi
# }

# Notify using swaync
notify_user() {
    if [[ "$(get_volume)" == "Muted" ]]; then
        notify-send -e -h string:x-canonical-private-synchronous:volume_notif -u low -i "$(get_icon)" "Volume: Muted"
    else
        notify-send -e -h int:value:"$(get_volume | sed 's/%//')" -h string:x-canonical-private-synchronous:volume_notif -u low -i "$(get_icon)" "Volume: $(get_volume)"
    fi
}

# Increase Volume with notification
inc_volume_notify() {
    if [ "$(pactl get-sink-mute @DEFAULT_SINK@)" == "Mute: yes" ]; then
        pactl set-sink-mute @DEFAULT_SINK@ false
    fi
    pactl set-sink-volume @DEFAULT_SINK@ +5% && notify_user
}

# Decrease Volume with notification
dec_volume_notify() {
    if [ "$(pactl get-sink-mute @DEFAULT_SINK@)" == "Mute: yes" ]; then
        pactl set-sink-mute @DEFAULT_SINK@ false
    fi
    pactl set-sink-volume @DEFAULT_SINK@ -5% && notify_user
}

# Increase Volume
inc_volume() {
    if [ "$(pactl get-sink-mute @DEFAULT_SINK@)" == "Mute: yes" ]; then
        pactl set-sink-mute @DEFAULT_SINK@ false
    fi
    pactl set-sink-volume @DEFAULT_SINK@ +5%
}

# Decrease Volume
dec_volume() {
    if [ "$(pactl get-sink-mute @DEFAULT_SINK@)" == "Mute: yes" ]; then
        pactl set-sink-mute @DEFAULT_SINK@ false
    fi
    pactl set-sink-volume @DEFAULT_SINK@ -5%
}

# Toggle Mute
toggle_mute() {
    if [ "$(pactl get-sink-mute @DEFAULT_SINK@)" == "Mute: no" ]; then
        pactl set-sink-mute @DEFAULT_SINK@ true
        notify-send -a -h -i "$iDIR/muted-speaker.svg" "Volume Switched OFF"
    elif [ "$(pactl get-sink-mute @DEFAULT_SINK@)" == "Mute: yes" ]; then
        pactl set-sink-mute @DEFAULT_SINK@ false
        notify-send -a -h -i "$iDIR/unmuted-speaker.svg" "Volume Switched ON"
    fi
}

# Toggle Mic
toggle_mic() {
    if [ "$(pactl get-source-mute @DEFAULT_SOURCE@)" == "Mute: no" ]; then
        pactl set-source-mute @DEFAULT_SOURCE@ true
        notify-send -e -u low -i "$iDIR/muted-mic.svg" "Microphone Switched OFF"
    elif [ "$(pactl get-source-mute @DEFAULT_SOURCE@)" == "Mute: yes" ]; then
        pactl set-source-mute @DEFAULT_SOURCE@ false
        notify-send -e -u low -i "$iDIR/unmuted-mic.svg" "Microphone Switched ON"
    fi
}

# Get Mic Icon
get_mic_icon() {
    volume=$(pactl get-source-volume @DEFAULT_SOURCE@ | grep -oP '\d+%' | head -1 | tr -d '%')
    if [[ "$volume" -eq "0" ]]; then
        echo "$iDIR/muted-mic.svg"
    else
        echo "$iDIR/unmuted-mic.svg"
    fi
}

# Get Microphone Volume
get_mic_volume() {
    volume=$(pactl get-source-volume @DEFAULT_SOURCE@ | grep -oP '\d+%' | head -1 | tr -d '%')
    if [[ "$volume" -eq "0" ]]; then
        echo "Muted"
    else
        echo "${volume}%"
    fi
}

# Notify for Microphone
notify_mic_user() {
    volume=$(get_mic_volume)
    icon=$(get_mic_icon)
    notify-send -a -r 91190 -t 800 -i "$icon" "Mic=vel: $volume"
}

# Increase MIC Volume with notification
inc_mic_volume_notify() {
    if [ "$(pactl get-source-mute @DEFAULT_SOURCE@)" == "Mute: yes" ]; then
        pactl set-source-mute @DEFAULT_SOURCE@ false
    fi
    pactl set-source-volume @DEFAULT_SOURCE@ +5% && notify_mic_user
}

# Decrease MIC Volume with notification
dec_mic_volume_notify() {
    if [ "$(pactl get-source-mute @DEFAULT_SOURCE@)" == "Mute: yes" ]; then
        pactl set-source-mute @DEFAULT_SOURCE@ false
    fi
    pactl set-source-volume @DEFAULT_SOURCE@ -5% && notify_mic_user
}

# Increase MIC Volume
inc_mic_volume() {
    if [ "$(pactl get-source-mute @DEFAULT_SOURCE@)" == "Mute: yes" ]; then
        pactl set-source-mute @DEFAULT_SOURCE@ false
    fi
    pactl set-source-volume @DEFAULT_SOURCE@ +5%
}

# Decrease MIC Volume
dec_mic_volume() {
    if [ "$(pactl get-source-mute @DEFAULT_SOURCE@)" == "Mute: yes" ]; then
        pactl set-source-mute @DEFAULT_SOURCE@ false
    fi
    pactl set-source-volume @DEFAULT_SOURCE@ -5%
}

# Execute accordingly
if [[ "$1" == "--get" ]]; then
    get_volume
elif [[ "$1" == "--inc" ]]; then
    inc_volume
elif [[ "$1" == "--dec" ]]; then
    dec_volume
elif [[ "$1" == "--toggle" ]]; then
    toggle_mute
elif [[ "$1" == "--toggle-mic" ]]; then
    toggle_mic
elif [[ "$1" == "--get-icon" ]]; then
    get_icon
elif [[ "$1" == "--get-mic-icon" ]]; then
    get_mic_icon
elif [[ "$1" == "--mic-inc" ]]; then
    inc_mic_volume
elif [[ "$1" == "--mic-dec" ]]; then
    dec_mic_volume
else
    get_volume
fi
