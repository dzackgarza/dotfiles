#!/bin/bash
xinput set-prop "ELAN Touchscreen Pen stylus" --type=float "Coordinate Transformation Matrix" 0.708749 0.000000 0.000000 0.000000 0.500000 0.500000 0.000000 0.000000 \1.000000
xinput set-prop "ELAN Touchscreen Pen eraser" --type=float "Coordinate Transformation Matrix" 0.708749 0.000000 0.000000 0.000000 0.500000 0.500000 0.000000 0.000000 \1.000000
xsetwacom set "ELAN Touchscreen Pen stylus" Button 2 3
