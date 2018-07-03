# Raspberry Pi

The following notes describe how to set up the Raspberry Pi used as the main controller on the ZeroOne project.

## Installing the Raspberry Pi Raspbian image

The ZeroOne project uses the [Stretch Lite](https://downloads.raspberrypi.org/raspbian_lite_latest) version of the [Raspian](https://www.raspberrypi.org/downloads/raspbian/) operating system.

Use an SD-Card of at least 8GB in capacity and use [Etcher](https://etcher.io/) on MacOS to write the image to the SD-Card. 

Before booting the SD-Card it might be useful to follow the additional steps to configure and enable WiFi access upon initial boot, see below for further

## Updating and Upgrading the image

After the installation it is necessary to upgrade and update Raspbian using the following commands:

> \# sudo apt-get update \
> \# sudo apt-get dist-upgrade

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

It should be easily possible to find the Pi by looking at the hostname, if this method eludes you the [following](https://gist.github.com/dolmen/511a94761f8089964a03) shell snippet should help (although it didn't appear to work on Mac OS):

```
# Scan the local network to put IPs in the ARP cache
nmap -sn -n $(route | sed -n '/^[1-9]/{s/ .*$//p;q}')/24 >/dev/null
# Look for Pi' MACs in the arp cache
arp -n | grep -i 'b8:27:eb:'
```

### Accessing the Pi with Ethernet

The easiest method of getting access to the Pi is via Ethernet connection. Use a dedicated network port on your host machine to connect directly to the Ethernet socket on the Pi, ensuring that the network port has been configured to provide DHCP services (this depends on your OS but generally ticking the boxes to allow 'internet connection sharing' ought to do the trick). Use the OS to determine the host RFC 1918 IP address (on my Mac this was 192.168.3.1) and with the method described above verify that there exists a Pi device on that same subnet (in my case 192.168.3.10).

Use _ping_ to determine connectivity to the specified IP address. Additionally you may wish to use some method (_hosts_ file, etc) to assign a hostname to this device to avoid having to remember the IP address.

Use the following configuration on Mac OS to enable 'internet connection sharing':

![Sharing on Mac OS](https://raw.githubusercontent.com/colindomoney/ZeroOne/master/Documentation/images/Sharing.png)

## Setting up SSH on the Pi

### Setting up a Factory Build Pi
It is quite likely that your Pi will already be setup correctly with SSH; however if you are building a new Pi from a factory build Pi you need to perform the following steps:

The initial connection to the Raspberry Pi needs to be performed with the default Raspberry Pi factory credentials, namely:

__Username:__ pi \
__Password:__ raspberry

Upon access to the Pi the suggestion is to change the default password immediately using the following command:
> passwd

The password value used on this project is located in [secrets.yaml](https://github.com/colindomoney/ZeroOne/blob/master/secrets.yaml) file. 

It is also necessary to enable SSH on the Pi using:

> ssh-keygen

Accept all the defaults and use an empty passphrase. Also ensure the correct directory and file permissions are set as per [this article](https://www.raspberrypi.org/forums/viewtopic.php?t=23061). Usually this is simply the following:

```
~/.ssh/authorized_keys : 644
~/.ssh : 700
```

### Connecting to a Pre-configured Pi

If your Pi has already been configured (this will almost certainly be the case) then all that is necessary is to configure your SSH client to use the correct SSH private key. The details on how to extract this private key from the [secrets.yaml](https://github.com/colindomoney/ZeroOne/blob/master/secrets.yaml) file can be found [here](https://github.com/colindomoney/ZeroOne/blob/master/Documentation/Setting%20up%20Git-Crypt.md)

Add an entry to your SSH congig file to specify this file to be used for connections to the Pi either using a hostname or IP address, such as:

```
# cat ~/.ssh/config
Host rpi.local
        User pi
        IdentityFile /Users/colind/.ssh/id_rsa_zero-one
```
In the event of any problems turn on verbose debugging on the SSH client using the '-v' option, problems are often associated with directory and file permissions.

## Install the Python Environment

### Setting the Default Python Interpreter

Generally life goes better with newer versions of Python, such as 3.5 and above. The latest versions of Raspbian appear to ship with Python 3.5 but the default interpreter is still set to Python 2.7. The [following steps](https://linuxconfig.org/how-to-change-from-default-to-alternative-python-version-on-debian-linux) describe how to set the default to 3.5.

> \# update-alternatives --install /usr/bin/python python /usr/bin/python2.7 1 \
> \# update-alternatives --install /usr/bin/python python /usr/bin/python3.5 2 \
> \# sudo apt-get install python-dev \
> \# sudo update-alternatives --config python

Following the last command ensure that Python 3.5 is selected as the default, or option 0.

Verify this by getting the Python version as below:

```
# python -V
Python 3.5.3
```

### Install Python Pip

It is also necessary to install the Pip package manager for Python 3 using the following commands:

> \# sudo apt-get install python3-pip \
> \# sudo ln -s /usr/bin/pip3 /usr/local/bin/pip 

### Install the Package Dependencies

The Python code for this project has a few dependencies mostly on the [Pillow image library](http://python-pillow.org/) and they must be installed __prior__ to installing the Python packages as follows:

> \# sudo apt-get install libopenjp2-7-dev
> \# sudo apt install libtiff5
> \# sudo apt-get install libatlas-base-dev
> \# sudo apt install python3-numpy

### Install the Packages

The Python packages for the ZeroOne project are contained in a requirements file and can be installed using the following command:

> \# sudo pip install -U -r requirements.txt

## Getting the ZeroOne code

Create a directory in the home directory of the Pi called 'ZeroOne' viz.
> /home/pi/ZeroOne/

In the home directory ('/home/pi') clone the ZeroOne repository as follows:
> git clone git@github.com:colindomoney/ZeroOne.git /home/pi/temp

Then execute the following commands to copy the contents of the 'Controller' directory to the 'ZeroOne' folder root:

> cd /home/pi \
> mkdir ZeroOne \
> cp -R temp/Controller/* ./ZeroOne/. \
> rm -rf temp/

## Build the FadeCandy Server

[FadeCandy](https://github.com/scanlime/fadecandy) is a server responsible for driving bit patterns to the Neopixel display using the USB interfaces on the Pi. To use FadeCandy it is necessary to clone the repo, build from source, and execute using the configuration file. 

In order to build the FadeCandy server execute the following steps:

> cd /home/pi/ZeroOne/ \
> git clone git@github.com:scanlime/fadecandy.git \
> cd fadecandy/server \
> make submodules \
> make

### Test the FadeCandy Server

Copy the configuration file to the server folder using these commands:

> cd /home/pi/ZeroOne/ \
> cp FadeCandy_Config/zero-one_config.json fadecandy/server/.

To test the FadeCandy server execcute the following commands:

> cd /home/pi/ZeroOne/ 
> fadecandy/server/fcserver fadecandy/server/zero-one_config.json

## Enabling USB 'hotplug' 

In order to ensure that the USB devices are assigned correct permissions it is necessary to add a configuration file for the [udev](https://linux.die.net/man/8/udev) driver as follows:

```
# cat /etc/udev/rules.d/50-usb-perms.rules
SUBSYSTEM=="usb", ATTR{idVendor}=="1d50", ATTR{idProduct}=="607a", MODE="0777"
```

