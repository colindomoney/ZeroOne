#!/usr/bin/env bash

echo "> Running startup.sh - $(date)" >> /home/pi/startup.log

python /home/pi/ZeroOne/ZeroOneController.py --config ./config-pi.ini &

echo "> Done with startup.sh - $(date)" >> /home/pi/startup.log

exit 0
