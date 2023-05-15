#!/bin/bash

pkill mono;
pkill dropbox;
echo "power off" | bluetoothctl;
nmcli radio wifi off;
sudo cpupower frequency-set -u 400Mhz;
