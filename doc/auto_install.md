Automatic installation of Raspbian to a hard-disk
-------------------------------------------------

The preparation of a hard-disk as described above is not very complicated,
but it can be fully automated. As an added benefit, also the operating
system runs from the disk. This will use the micro SDHC only for booting
and will certainly extend the lifetime of the card.

On a Linux sytem, download the git-project called `apiinst`

    git clone https://github.com/bablokb/apiinst.git

Now attach your micro SDHC card to your PC (we will assume it uses
`/dev/sdb`) and then attach your hard-disk to the PC. In our example
it will use `/dev/sdc`. Please make sure that these device names
are correct, else you will risk loosing all your data on your PC. Existing
data on the devices will always be deleted.

To install Raspbian and prepare a data-partition on the disk, just run

    sudo apiinst/bin/apiinst -i /path/to/20160527-raspbian-jessie-lite.zip \
         -B /dev/sdb -t /dev/sdc -D 150G

Adapt the size of the data-partition (option `-D`) to your needs. The
command above will add all remaining space to the root-partition of the
system.
