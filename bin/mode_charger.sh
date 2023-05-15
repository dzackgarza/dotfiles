#!/bin/bash

sparkleshare &
dropbox &
echo "power on" | bluetoothctl;
nmcli radio wifi on;
sudo cpupower frequency-set -u 4.6Ghz;
