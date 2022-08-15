#!/usr/bin/env python3

import os

# typedef struct {
	# char name[100];
	# char mode[8];
	# char uid[8];
	# char gid[8];
	# char size[12];
	# char mtime[12];
	# char chksum[8];
	# char typeflag;
	# char linkname[100];
	# char magic[6];
	# char version[2];
	# char uname[32];
	# char gname[32];
	# char devmajor[8];
	# char devminor[8];
	# char prefix[155];
	# char pad[12];
# } TarHeader;

BLOCKSIZE = 512

# POSIX 1003.1-1988
USTAR_DIR_MODE = b"0000755"
USTAR_FILE_MODE = b"0000644"
USTAR_UID = b"0000000"
USTAR_GID = b"0000000"
USTAR_MTIME = b"00000000000"
USTAR_CHKSUM = b"000000"
USTAR_DIR_TYPE = b" 5"
USTAR_FILE_TYPE = b" 0"
USTAR_MAGIC = b"ustar"
USTAR_VERSION = b"00"
USTAR_DEVMAJOR = b"0000000"
USTAR_DEVMINOR = b"0000000"

def TarAddHeader(tarfile, filename):
	tarfile.write(bytes(filename, "utf-8"))
	tarfile.seek(100, os.SEEK_SET)
	tarfile.write(USTAR_FILE_MODE)
	tarfile.seek(108, os.SEEK_SET)
	tarfile.write(USTAR_UID)
	tarfile.seek(116, os.SEEK_SET)
	tarfile.write(USTAR_GID)
	tarfile.seek(124, os.SEEK_SET)
	tarfile.write(USTAR_MTIME)
	tarfile.seek(136, os.SEEK_SET)
	tarfile.write(USTAR_MTIME)
	tarfile.seek(148, os.SEEK_SET)
	tarfile.write(USTAR_CHKSUM)
	tarfile.seek(155, os.SEEK_SET)
	tarfile.write(USTAR_FILE_TYPE)
	tarfile.seek(257, os.SEEK_SET)
	tarfile.write(USTAR_MAGIC)
	tarfile.seek(263, os.SEEK_SET)
	tarfile.write(USTAR_VERSION)
	tarfile.seek(329, os.SEEK_SET)
	tarfile.write(USTAR_DEVMAJOR)
	tarfile.seek(337, os.SEEK_SET)
	tarfile.write(USTAR_DEVMINOR)
	tarfile.seek(512, os.SEEK_SET)

def TarAddFile(tarfile, filename):
	# open the file
	stream = open(filename, "rb")

	# retrieve file size
	stream.seek(0, os.SEEK_END)
	filesize = stream.tell()
	stream.seek(0, os.SEEK_SET)

	# write the file header
	TarAddHeader(tarfile, filename)

	# write the file
	tarfile.write(stream.read())

	# close the file
	stream.close()

	# align by block size
	padsize = (filesize + (BLOCKSIZE - 1)) & ~(BLOCKSIZE - 1)
	padsize -= filesize
	tarfile.seek(tarfile.tell() + padsize)

def TarEmptyBlock(tarfile):
	closesize = 512
	while closesize != 0:
		tarfile.write(b"\x00")
		closesize -= 1

def main():
	tarfile = open("output.tar", "wb")

	TarAddFile(tarfile, "junk.bin")
	TarEmptyBlock(tarfile)

	tarfile.close()

if __name__ == "__main__":
	main()
