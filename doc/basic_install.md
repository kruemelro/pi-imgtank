Basic installation
------------------

Installation is quite simple. Grab the current version of
Raspbian-Jessie-Lite and install it to an micro SDHC card. Configure
the system to taste.

Then attach an external usb-disk, and execute the following command:

    sudo fdisk /dev/sda

If the disk is already partitioned, you should first delete all existing
partitions. Use the `p`-command (`print`) to check for existing partitions
and the `d`-command to delete them. Once the print-command does not show any
partitions anymore, create a new one with `n`. You can accept all defaults,
this will create a single partition which takes up all available
space. Leave the fdisk-program with the `w`-command (`write`). This
will erase all data already on the disk, so make sure you don't loose
any important data.

Next, you should format the partition, create a mount-point and
mount the partition:

    sudo mkfs.ext4 /dev/sda1
    sudo mkdir /data
    sudo mount /dev/sda1 /data

All space is now available in the `/data`-directory. Since the mount
is temporary, you should now open the file `/etc/fstab` with your
favorite editor andd add the following line

    /dev/sda1 /data ext4 user_xattr,noatime,acl 1 2

Reboot and check with the `df`-command that the external drive is
mounted and the space is available.

If you are a Linux-user you can automate all the above steps. For
details, see [auto_install.md](./auto_install.md 
 "Automatic installation of Raspbian to a hard-disk").
