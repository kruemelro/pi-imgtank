Raspberry Pi Imagetank
======================

What it is
----------

The imagetank is a backup solution for images based on a Raspberry Pi.
The basic idea is that you plug in your SD-card from your camera into the
Pi (using an USB adapter), and the Pi will automatically copy all
images to an attached HDD/SDD.

Since this is a headless system, the user interface has to be simple. The
imagetank uses an extension board called "Pibrella", which is
manufactured by Pimoroni. This board has a number of LEDs which we
use to signal state and a button, which we use for shutdown.

![Pi with Pibrella](images/pibrella.jpg "Pi with Pibrella")

You could also use the system without the extension board or use
a different solution like one of the simple TFT touch screens. In this
case you have to put tweak some of the scripts of this project.


Installation
------------

First, install your system as described in
[Basic installation](./doc/basic_install.md "Basic installation"). This
sets up your system and your HDD/SDD.

After basic installation, you need to install the files specific
to the image tank:

    sudo su -
    git clone https://github.com/bablokb/pi-imgtank.git
    cd pi-imgtank
    sudo tools/install-piimgtank
    exit

This will install some scripts and configuration files needed
by the imagetank. It also configures a number of systemd-services
which will control the leds of the Pibrella-board and which take
care of copying the images.

The core of the tank is an udev-rule which will automatically start a
system-service (`/etc/systemd/system/copy_img2@.services`)
on plugin of a SD-card. That service in turn will start the
script `/usr/local/sbin/copy_img2` which does all the copying.

Note that there are two versions of the copy script: `copy_img` and `copy_img2`.
The first version does not change filenames while copying images,
**you therefore risk data-loss if you reset the image-numbers within
your camera or if you use multiple cameras which use the same
naming-scheme!**

Make sure that `/etc/systemd/system/copy_img2@.services`
points to the correct script (the service name is not relevant,
you have to change the value of `ExecStart` within that file).


### Using the Imagetank as an Access-Point ###

Since the Pi3 has a builtin WIFI chip, we can set it up as an access-point.
This allows access to the images even when not connected to a
dedicated network. For instructions, see
[Setting up an Access-Point](./doc/hostapd_install.md 
"Setting up an Access-Point").

### Web access to your images ###

If you want to browse the images on the imagetank, you have to install
a webserver on the system. You can find the necessary instructions
in the document [Installing a Webserver](./doc/web_install.md 
"Installing a Webserver").

Once installed, you can also upload files using the web-interface. All
uploaded files will also be moved in the same way as files from a
SD-card.

### Using the Imagetank as a Fileserver ###

The imagetank is meant as a backup solution. In case you need to recover
your files, a Samba-server comes in handy to access your images from
any computer within your network. You can find a setup instruction
[here](./doc/samba_install.md "Installing Samba").


Operation
---------

Now shut down and if not already done, install the Pibrella extension. If
you now reconnect power you should see the red led blinking for a few
seconds. After that, the red turns off and the green led turns on. The
system is now ready.

Insert a SDHC card from your digital camera into an USB-adapter and plug
it into the Pi. The orange led should now start to blink slowly. After all
files are copied, the led stops blinking and the green led comes on again.
Now it is safe to remove the USB-adapter.

The leds of the Pibrella hat always reflects the current state of the
system. You can see a  graphical representation of the various states in
the following image.

![System states with transitions](images/states.png "System states with transitions")

You can log into your system using ssh and see log-messages of the copy-script:

    sudo journalctl SYSLOG_IDENTIFIER=copy_img

or

    sudo journalctl SYSLOG_IDENTIFIER=copy_img2

(depending on which version of the copy-script you are using).


