Setting up an Access-Point
==========================

To set up an access-point, edit `tools/install-hostapd` to your needs and run

    sudo su -
    cd pi-imgtank
    tools/install-hostapd

This will install `hostapd` and `dnsmasq` and configure both packages.

**Note that you definitely should at least change the wlan-password
(variable `wpa_passphrase`) in the installation script!**

If you also install the [webserver](./doc/web_install.md 
"Installing a Webserver"), you can access the images using the address 

    http://pi-imgtank/

This works since `dnsmasq` will resolve all hostnames from `/etc/hosts`
and the installation script adds `pi-imgtank` to `/etc/hosts`.

**If you are not using a Pi3, you have to provide your own WLAN-dongle.
The standard hostapd-package might not work in this case.**

For a workaround, see
[https://github.com/bablokb/rpihotspot](https://github.com/bablokb/rpihotspot "https://github.com/bablokb/rpihotspot").
