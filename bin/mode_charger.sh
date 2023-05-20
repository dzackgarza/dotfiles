#!/bin/bash

sparkleshare &
dropbox &
rfkill unblock all; echo "power on\r\n connect 88:C9:E8:2D:78:82" | bluetoothctl;
nmcli radio wifi on;
sudo cpupower frequency-set -u 4.6Ghz;
