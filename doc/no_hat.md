Using the Imagetank without Additional Hardware
-----------------------------------------------

Without additional hardware, you loose the status information of the
LEDs. In a future version of the project, the green LED of the Pi
will be used for that. In the meantime, be sure to wait after any
operation long enough so that it will complete safely.

You also loose the ability to shutdown the system using a key. There are
two alternatives available:

  - use the web-interface. Here you will find in System-menu two entries:
    shutdown and reboot. They both act without asking any questions, so
    be prepared.

  - Activate the udev-rule in `/etc/udev/rules.d/99-usbhalt.rules` (just
    remove the hash at the beginning of the line of the rule). In this
    case, the system shuts down automatically after you remove your
    usb-adapter with the SD-card.

