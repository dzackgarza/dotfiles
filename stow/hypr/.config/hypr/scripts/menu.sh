#!/usr/bin/env bash

dir="$HOME/.config/rofi/menu"
theme='style-1'

## Run
rofi \
    -show drun \
    -drun-display-format '{name} - {comment}' \
    -theme ${dir}/${theme}.rasi
