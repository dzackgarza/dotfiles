#!/bin/bash
xsetwacom set "ELAN Touchscreen" MapToOutput eDP1
xsetwacom set "ELAN Touchscreen stylus" MapToOutput eDP1
xsetwacom set "ELAN Touchscreen eraser" MapToOutput eDP1

matrix=$(xinput list-props "ELAN Touchscreen" | grep 'Coordinate Transformation Matrix' | cut -d ':' -f 2 | xargs)

xinput set-prop "ELAN Touchscreen" --type=float "Coordinate Transformation Matrix" $matrix
xinput set-prop "ELAN Touchscreen stylus" --type=float "Coordinate Transformation Matrix" $matrix
xinput set-prop "ELAN Touchscreen eraser" --type=float "Coordinate Transformation Matrix" $matrix
