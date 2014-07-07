#!/bin/bash

mkdir -p bin dev etc lib lib64 mnt/root proc root sbin sys
cp -aL /bin/busybox bin/
echo "#!/bin/busybox sh

# Mount the /proc and /sys filesystems.
mount -t proc none /proc
mount -t sysfs none /sys

# Do your stuff here.
echo "This script mounts rootfs and boots it up, nothing more!"

# Mount the root filesystem.
mount -o ro /dev/sda1 /mnt/root

# Clean up.
umount /proc
umount /sys

# Boot the real thing.
exec switch_root /mnt/root /sbin/init" > init
chmod u+x init

