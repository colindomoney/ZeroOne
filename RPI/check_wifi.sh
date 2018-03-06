ping -c4 192.168.9.4 > /dev/null
 
if [ $? != 0 ] 
then
    echo "No network connection, restarting wlan0" 2>&1 | tee './check_wifi.log'
    sudo ifconfig 'wlan0' down
    sleep 2
    sudo ifconfig 'wlan0' up
fi
