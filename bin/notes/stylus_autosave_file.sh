#!/bin/bash

xdotool search --name Write && xdotool key --window $(xdotool search --name Write) space
