#!/usr/bin/env python3

""" itar -- Create idempotent tape archives

Output archive will have well defined sort order
and neutral metadata for files. This helps to enable
deterministic outcomes to verify known builds within
your build chain.

ref: https://reproducible-builds.org/docs/archives/

"""

import os
import argparse

BLOCKSIZE = 512
RECORDS = 20
TAPESIZE = RECORDS * BLOCKSIZE

# POSIX 1003.1-1988
USTAR_DIR_MODE = "0000755"
USTAR_FILE_MODE = "0000644"
USTAR_UID = "0000000"
USTAR_GID = "0000000"
USTAR_MTIME = "00000000000"
USTAR_CHKSUM = b"       "
USTAR_DIR_TYPE = " 5"
USTAR_FILE_TYPE = " 0"
USTAR_MAGIC = "ustar"
USTAR_VERSION = "00"
USTAR_DEVMAJOR = "0000000"
USTAR_DEVMINOR = "0000000"

# Convert a decimal integer into an octal string
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

# Simple checksum using sum of all bytes in header
def ComputeChksum(data, sum):
	for c in data:
		sum += c
	return sum

# Write a given string to the header and update checksum
def TarHdrChunk(tarfile, string, offset, chksum):
	data = bytes(string, "utf-8")
	tarfile.seek(offset, os.SEEK_SET)
	tarfile.write(data)
	return ComputeChksum(data, chksum)

# Python conveniently has no structs, so we have to manually
# hardcode header offsets hence the mess below
def TarAddHeader(tarfile, filename, ofilesize, filemode, filetype):
	hdrstart = tarfile.tell()

	# Fixup the file name to be consistent on all platforms
	filename = filename.replace("\\", "/") # Always use forward slash
	filename = filename.lstrip("./") # Remove leading prefix

	chksum = 0 # Initialize checksum to zero
	chksum = TarHdrChunk(tarfile, filename,       hdrstart + 0,   chksum)
	chksum = TarHdrChunk(tarfile, filemode,       hdrstart + 100, chksum)
	chksum = TarHdrChunk(tarfile, USTAR_UID,      hdrstart + 108, chksum)
	chksum = TarHdrChunk(tarfile, USTAR_GID,      hdrstart + 116, chksum)
	chksum = TarHdrChunk(tarfile, ofilesize,      hdrstart + 124, chksum)
	chksum = TarHdrChunk(tarfile, USTAR_MTIME,    hdrstart + 136, chksum)
	chksum = TarHdrChunk(tarfile, filetype,       hdrstart + 155, chksum)
	chksum = TarHdrChunk(tarfile, USTAR_MAGIC,    hdrstart + 257, chksum)
	chksum = TarHdrChunk(tarfile, USTAR_VERSION,  hdrstart + 263, chksum)
	chksum = TarHdrChunk(tarfile, USTAR_DEVMAJOR, hdrstart + 329, chksum)
	chksum = TarHdrChunk(tarfile, USTAR_DEVMINOR, hdrstart + 337, chksum)

	# Checksum is pre-computed using blanks (spaces)
	tarfile.seek(hdrstart + 148, os.SEEK_SET)
	chksum = ComputeChksum(USTAR_CHKSUM, chksum)
	tarfile.write(bytes(DecimalToOctal(chksum, 6), "utf-8"))

	tarfile.seek(hdrstart + 512, os.SEEK_SET)

# Write file data to the tar file
def TarAddFile(tarfile, filename):
	# open the file
	stream = open(filename, "rb")

	# retrieve file size
	stream.seek(0, os.SEEK_END)
	filesize = stream.tell()
	stream.seek(0, os.SEEK_SET)

	ofilesize = DecimalToOctal(filesize, 11)

	# write the file header
	TarAddHeader(tarfile, filename, ofilesize, USTAR_FILE_MODE, USTAR_FILE_TYPE)

	# write the file
	tarfile.write(stream.read())

	# close the file
	stream.close()

	# align by block size
	padsize = (filesize + (BLOCKSIZE - 1)) & ~(BLOCKSIZE - 1)
	padsize -= filesize
	tarfile.seek(tarfile.tell() + padsize)

# Write directory entry to the tar file
def TarAddDir(tarfile, filename):
	ofilesize = DecimalToOctal(0, 11)

	# write the file header (append slash to directory)
	TarAddHeader(tarfile, filename + "/", ofilesize, USTAR_DIR_MODE, USTAR_DIR_TYPE)

# Pad archive in multiples of TAPESIZE which specifies
# the maximum data to be recorded on an individual tape
def TarCloseArchive(tarfile):
	closesize = tarfile.tell()
	closesize += TAPESIZE
	closesize -= closesize % TAPESIZE
	tarfile.seek(closesize - 1, os.SEEK_SET)
	tarfile.write(b"\x00")
	tarfile.close()

# Append everything to the tar file, using default umask
# of 022 (755 for folders, 644 for everything else)
def TarBuildArchive(tarfile, filelist):
	for f in filelist:
		if os.path.isfile(f):
			TarAddFile(tarfile, f)
		elif os.path.isdir(f):
			TarAddDir(tarfile, f)

# Recursively build a list of everything the user specified
# and sort using C collation, exit on failure
def GetFileList(dirname):
	try:
		os.chdir(dirname)
	except:
		print("Could not change to directory \"%s\"" % (dirname))
		quit()

	filelist = []
	for root, dirs, files in os.walk("."):
		for filename in files:
			filelist.append(os.path.join(root, filename))
		for dirname in dirs:
			filelist.append(os.path.join(root, dirname))

	filelist.sort()
	return filelist

# Create the destination tar file, exit on failure
def TarInitFile(filename):
	try:
		tarfile = open(filename, "wb")
	except:
		print("Could not create output archive \"%s\"" % (filename))
		quit()

	return tarfile

def main():
	parser = argparse.ArgumentParser(description='Creates idempotent tar file.')
	parser.add_argument('outfile', help='Name of output file')
	parser.add_argument('inputdir', help='Location of directory to archive')
	args = vars(parser.parse_args())

	tarfile = TarInitFile(args["outfile"])
	filelist = GetFileList(args["inputdir"])

	TarBuildArchive(tarfile, filelist)
	TarCloseArchive(tarfile)

if __name__ == "__main__":
	main()
