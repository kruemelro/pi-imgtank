Install Samba as a Fileserver
=============================

To install and configure samba, run

    sudo su -
    cd pi-imgtank
    tools/install-samba

Note that this is a very simple and insecure setup, since it allows
read/write access to the backuped images for everyone without any password.
If you need better security, change /etc/samba/smb.conf accordingly.

Please set 'guest account' to the owner of /data/images (normally pi).

