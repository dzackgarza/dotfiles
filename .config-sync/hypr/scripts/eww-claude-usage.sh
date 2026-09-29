#!/usr/bin/env bash
set -euo pipefail

CONFIG_DIR="/home/dzack/.config/hypr/eww/claude-usage"

eww -c "$CONFIG_DIR" daemon --restart
eww -c "$CONFIG_DIR" open claude_usage
