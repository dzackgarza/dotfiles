#!/bin/bash

sudo rfkill block bluetooth && sleep 0.2 && sudo rfkill unblock bluetooth
echo -e "power off\n" | bluetoothctl;
sleep 1
sudo systemctl restart bluetooth;
sleep 1
echo -e "power on\n" | bluetoothctl;
sleep 1
echo -e "connect E8:AB:FA:28:49:DC" | bluetoothctl;
echo -e "connect 12:34:20:01:4D:9D" | bluetoothctl;


