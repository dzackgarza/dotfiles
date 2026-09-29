#!/bin/bash

# Websites for rofi menu
declare -a options=(
"gmail"
"hackmd.io"
"chatgpt"
"claude"
"perplexity"
"neverssl"
"songsterr"
"youtube"
)

# Rofi menu
choice=$(printf "%s\n" "${options[@]}" | rofi -dmenu -i -p "Open website")

# Open choice in chromium
if [ -n "$choice" ]; then
    case $choice in
        "gmail") chromium "https://mail.google.com" ;;
        "hackmd.io") chromium "https://hackmd.io" ;;
        "chatgpt") chromium "https://chat.openai.com" ;;
        "claude") chromium "https://claude.ai" ;;
        "perplexity") chromium "https://www.perplexity.ai" ;;
        "neverssl") chromium "http://neverssl.com" ;;
        "songsterr") chromium "https://www.songsterr.com" ;;
        "youtube") chromium "https://www.youtube.com" ;;
    esac
fi
