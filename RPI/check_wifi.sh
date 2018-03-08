#!/bin/bash

ping -c4 8.8.8.8 > /dev/null

if [ $? != 0 ]
then
    echo "No network connection, rebooting at" $(date) 2>&1 | tee -a '/home/pi/logs/check_wifi.log'
    sleep 2
    sudo reboot
fi
