#!/bin/bash

sudo systemctl restart bluetooth;
sudo rfkill block bluetooth && sleep 0.2 && sudo rfkill unblock bluetooth
echo -e "power off\n" | bluetoothctl;
sleep 1
sudo systemctl restart bluetooth;
sleep 1
echo -e "power on\n" | bluetoothctl;
sleep 1
echo -e "connect E8:AB:FA:2B:37:26" | bluetoothctl;
echo -e "connect 12:34:20:01:4D:9D" | bluetoothctl;
echo -e "connect 00:02:5B:31:C2:65" | bluetoothctl;


