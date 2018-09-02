#!/bin/bash
xsetwacom set "ELAN Touchscreen Pen stylus" MapToOutput eDP1
xsetwacom set "ELAN Touchscreen Pen eraser" MapToOutput eDP1

matrix=$(xinput list-props "ELAN Touchscreen" | grep 'Coordinate Transformation Matrix' | cut -d ':' -f 2 | xargs)

xinput set-prop "ELAN Touchscreen Pen stylus" --type=float "Coordinate Transformation Matrix" $matrix
xinput set-prop "ELAN Touchscreen Pen eraser" --type=float "Coordinate Transformation Matrix" $matrix
