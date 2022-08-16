#!/bin/sh

rm -f gnu.tar

tar -rf gnu.tar --format=ustar --mode=644 --mtime="UTC 1970-01-01" --numeric-owner --owner=0 --group=0 --no-recursion junk.bin
tar -rf gnu.tar --format=ustar --mode=644 --mtime="UTC 1970-01-01" --numeric-owner --owner=0 --group=0 --no-recursion junk.bin
