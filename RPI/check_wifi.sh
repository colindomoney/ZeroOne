#!/bin/bash

ping -c4 192.168.9.4 > /dev/null

if [ $? != 0 ]
then
    echo "No network connection, rebooting at" $(date) 2>&1 | tee -a '/home/pi/logs/check_wifi.log'
    sleep 2
    sudo reboot
fi
