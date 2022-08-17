#!/bin/sh

# create a metadata-free TAR with gnu-tar to compare against

rm -f gnu.tar

tar -cf gnu.tar --format=ustar \
	--mode=644 --mtime="UTC 1970-01-01" \
	--numeric-owner --owner=0 --group=0 \
	--no-recursion junk.bin
