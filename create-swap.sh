#!/bin/sh
sudo su
fallocate -l 2G /mnt/2GB.swap
mkswap /mnt/2GB.swap
swapon /mnt/2GB.swap
/mnt/2GB.swap  none  swap  sw 0  0
echo vm.swappiness=10 >> /etc/sysctl.conf
swapon -s
exit

