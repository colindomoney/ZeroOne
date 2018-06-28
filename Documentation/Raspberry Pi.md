# Topics

1. Which version of Pi OS to use
1. How to install it and update it
1. Setting up WiFi on the Pi
1. Accessing the Pi with Ethernet
1. Installing the FastLED driver
    1. Building it 
    1. USB permissions
1. Setting up SSH
1. Getting the ZeroOne code

The following notes describe how to set up the Raspberry Pi used as the main controller on the ZeroOne project

## Installing the Raspberry Pi Raspbian image

The ZeroOne project uses the [Stretch Lite](https://downloads.raspberrypi.org/raspbian_lite_latest) version of the [Raspian](https://www.raspberrypi.org/downloads/raspbian/) operating system.

Use an SD-Card of at least 8GB in capacity and use [Etcher](https://etcher.io/) on MacOS to write the image to the SD-Card. 

Before booting the SD-Card it might be useful to follow the additional steps to configure and enable WiFi access upon initial boot, see below for further

## Updating and Upgrading the image

## Connecting the Pi to a Network

### Setting up WiFi on the Pi

With more recent distributions of the Raspberry Pi it is possible to configure the Raspbian boot image to automatically connect to a WiFI access point upon initial boot thereby allowing completely 'headless' operation. The process involves writing two files to the root partition of the image, the following articles describe the process in greater detail:

[Article One](https://medium.com/@danidudas/install-raspbian-jessie-lite-and-setup-wi-fi-without-access-to-command-line-or-using-the-network-97f065af722e) \
[Article Two](https://howchoo.com/g/ndy1zte2yjn/how-to-set-up-wifi-on-your-raspberry-pi-without-ethernet) \
[Article Three](
https://howchoo.com/g/ote0ywmzywj/how-to-enable-ssh-on-raspbian-jessie-without-a-screen)

### Changing Your WiFi Settings

The Raspbian WiFi settings are maintained in the following file:

> /etc/wpa_supplicant/wpa_supplicant.conf

A typical configuration file is shown below:

```
ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev
network={
    ssid="YOUR_NETWORK_NAME"
    psk="YOUR_PASSWORD"
    key_mgmt=WPA-PSK
}
```

### Finding your Pi on the Network

Unless you are using a fixed IP address in your Pi configuration the Pi will get a dynamic IP address from the host network using DHCP. In a 'headless' setup it will be impossible to know ahead of time which IP address has been assigned to the Pi. The best method to 'find' the Pi is to use the following command:

> arp -a

It should be easily possible to find the Pi by looking at the hostname, if this method eludes you the [following](https://gist.github.com/dolmen/511a94761f8089964a03) shell snippet should help:

```
# Scan the local network to put IPs in the ARP cache
nmap -sn -n $(route | sed -n '/^[1-9]/{s/ .*$//p;q}')/24 >/dev/null
# Look for Pi' MACs in the arp cache
arp -n | grep -i 'b8:27:eb:'
```

### Accessing the Pi with Ethernet

The easiest method of getting access to the Pi is via Ethernet connection. Use a dedicated network port on your host machine to connect directly to the Ethernet socket on the Pi, ensuring that the network port has been configured to provide DHCP services (this depends on your OS but generally ticking the boxes to allow 'internet connection sharing' ought to do the trick). Use the OS to determine the host RFC 1918 IP address (on my Mac this was 192.168.3.1) and with the method described above verify that there exists a Pi device on that same subnet (in my case 192.168.3.10).

Use _ping_ to determine connectivity to the specified IP address. Additionally you may wish to use some method (_hosts_ file, etc) to assign a hostname to this device to avoid having to remember the IP address.

## Setting up SSH on the Pi

## Install the Pi Build Tools

* General build tools

* Python build tools

> sudo apt-get install python-dev

https://linuxconfig.org/how-to-change-from-default-to-alternative-python-version-on-debian-linux

* FadeCandy build tools

## Installing the FastLED driver
1. Building it 
1. USB permissions

## Getting the ZeroOne code