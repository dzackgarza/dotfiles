#!/bin/bash
xsetwacom set "ELAN Touchscreen" MapToOutput eDP1
xsetwacom set "ELAN Touchscreen stylus" MapToOutput eDP1
xsetwacom set "ELAN Touchscreen eraser" MapToOutput eDP1

matrix1=$(xinput list-props "ELAN Touchscreen" | grep 'Coordinate Transformation Matrix' | cut -d ':' -f 2 | xargs)

matrix=$(sage -c  "M = Matrix(RR, 3, [$matrix]); M2 = Matrix(RR, 3, [0, 1, 0, -1, 0, 1, 0, 0, 1]); print([round(x, 2) for x in (M*M2).list()])" | tr -d '[],')

xinput set-prop "ELAN Touchscreen" --type=float "Coordinate Transformation Matrix" $matrix
xinput set-prop "ELAN Touchscreen stylus" --type=float "Coordinate Transformation Matrix" $matrix
xinput set-prop "ELAN Touchscreen eraser" --type=float "Coordinate Transformation Matrix" $matrix

