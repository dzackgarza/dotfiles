#!/bin/bash

sudo systemctl restart bluetooth;
sudo rfkill block bluetooth && sleep 0.2 && sudo rfkill unblock bluetooth
echo -e "power off\n" | bluetoothctl;
sleep 1
sudo systemctl restart bluetooth;
sleep 1
echo -e "power on\n" | bluetoothctl;
sleep 1
echo -e "connect 74:45:CE:B3:15:D5" | bluetoothctl;


