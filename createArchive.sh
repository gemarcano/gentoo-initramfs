#!/bin/bash

cd /usr/src/initramfs/gentoo
find . -print0 | cpio --null -ov --format=newc | gzip -9 > ../initramfs.cpio.gz