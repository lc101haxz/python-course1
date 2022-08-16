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
RECORDS = 20
TAPESIZE = RECORDS * BLOCKSIZE

# POSIX 1003.1-1988
USTAR_DIR_MODE = b"0000755"
USTAR_FILE_MODE = b"0000644"
USTAR_UID = b"0000000"
USTAR_GID = b"0000000"
USTAR_MTIME = b"00000000000"
USTAR_CHKSUM = b"       "
USTAR_DIR_TYPE = b" 5"
USTAR_FILE_TYPE = b" 0"
USTAR_MAGIC = b"ustar"
USTAR_VERSION = b"00"
USTAR_DEVMAJOR = b"0000000"
USTAR_DEVMINOR = b"0000000"

def DecimalToOctal(n, len):
	temp = [0] * len

	i = 0
	while (n != 0):
		temp[i] = n % 8
		n = int(n / 8)
		i += 1

	temp.reverse()
	octal = ''.join(str(x) for x in temp)
	return octal

def ComputeChksum(data, sum):
	for c in data:
		sum += c
	return sum

def TarAddHeader(tarfile, filename, ofilesize):
	hdrstart = tarfile.tell()

	tarfile.write(bytes(filename, "utf-8"))
	chksum = ComputeChksum(bytes(filename, "utf-8"), 0)

	tarfile.seek(hdrstart + 100, os.SEEK_SET)
	tarfile.write(USTAR_FILE_MODE)
	chksum = ComputeChksum(USTAR_FILE_MODE, chksum)

	tarfile.seek(hdrstart + 108, os.SEEK_SET)
	tarfile.write(USTAR_UID)
	chksum = ComputeChksum(USTAR_UID, chksum)

	tarfile.seek(hdrstart + 116, os.SEEK_SET)
	tarfile.write(USTAR_GID)
	chksum = ComputeChksum(USTAR_GID, chksum)

	tarfile.seek(hdrstart + 124, os.SEEK_SET)
	tarfile.write(bytes(ofilesize, "utf-8"))
	chksum = ComputeChksum(bytes(ofilesize, "utf-8"), chksum)

	tarfile.seek(hdrstart + 136, os.SEEK_SET)
	tarfile.write(USTAR_MTIME)
	chksum = ComputeChksum(USTAR_MTIME, chksum)

	tarfile.seek(hdrstart + 155, os.SEEK_SET)
	tarfile.write(USTAR_FILE_TYPE)
	chksum = ComputeChksum(USTAR_FILE_TYPE, chksum)

	tarfile.seek(hdrstart + 257, os.SEEK_SET)
	tarfile.write(USTAR_MAGIC)
	chksum = ComputeChksum(USTAR_MAGIC, chksum)

	tarfile.seek(hdrstart + 263, os.SEEK_SET)
	tarfile.write(USTAR_VERSION)
	chksum = ComputeChksum(USTAR_VERSION, chksum)

	tarfile.seek(hdrstart + 329, os.SEEK_SET)
	tarfile.write(USTAR_DEVMAJOR)
	chksum = ComputeChksum(USTAR_DEVMAJOR, chksum)

	tarfile.seek(hdrstart + 337, os.SEEK_SET)
	tarfile.write(USTAR_DEVMINOR)
	chksum = ComputeChksum(USTAR_DEVMINOR, chksum)

	tarfile.seek(hdrstart + 148, os.SEEK_SET)
	chksum = ComputeChksum(USTAR_CHKSUM, chksum)
	tarfile.write(bytes(DecimalToOctal(chksum, 6), "utf-8"))

	tarfile.seek(hdrstart + 512, os.SEEK_SET)

def TarAddFile(tarfile, filename):
	# open the file
	stream = open(filename, "rb")

	# retrieve file size
	stream.seek(0, os.SEEK_END)
	filesize = stream.tell()
	stream.seek(0, os.SEEK_SET)

	ofilesize = DecimalToOctal(filesize, 11)

	# write the file header
	TarAddHeader(tarfile, filename, ofilesize)

	# write the file
	tarfile.write(stream.read())

	# close the file
	stream.close()

	# align by block size
	padsize = (filesize + (BLOCKSIZE - 1)) & ~(BLOCKSIZE - 1)
	padsize -= filesize
	tarfile.seek(tarfile.tell() + padsize)

def TarCloseArchive(tarfile):
	closesize = tarfile.tell()
	closesize += TAPESIZE
	closesize -= closesize % TAPESIZE
	tarfile.seek(closesize - 1, os.SEEK_SET)
	tarfile.write(b"\x00")

def main():
	tarfile = open("output.tar", "wb")

	TarAddFile(tarfile, "junk.bin")
	TarAddFile(tarfile, "junk.bin")
	TarCloseArchive(tarfile)

	tarfile.close()

if __name__ == "__main__":
	main()
