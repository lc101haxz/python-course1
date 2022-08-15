#!/usr/bin/env python

# Copyright (C) 2010 Sofian Brabez <sbz@6dev.net>
#
# This file is part of paramiko.
#
# Paramiko is free software; you can redistribute it and/or modify it under the
# terms of the GNU Lesser General Public License as published by the Free
# Software Foundation; either version 2.1 of the License, or (at your option)
# any later version.
#
# Paramiko is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR
# A PARTICULAR PURPOSE.  See the GNU Lesser General Public License for more
# details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with Paramiko; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301 USA.

import sys

# import only the needed functions
from binascii import hexlify
from optparse import OptionParser

from paramiko import DSSKey
from paramiko import RSAKey
# import class functions we'll need later
from paramiko.ssh_exception import SSHException
from paramiko.py3compat import u

# declare help output for --help
usage = """
%prog [-v] [-b bits] -t type [-N new_passphrase] [-f output_keyfile]"""

# setup default key output type
default_values = {
    "ktype": "dsa",
    "bits": 1024,
    "filename": "output",
    "comment": "",
}

# link key types to respective class
key_dispatch_table = {"dsa": DSSKey, "rsa": RSAKey}

# callback function to display key progress
def progress(arg=None):

	# write percent followed by special characters
    if not arg: # 0%
        sys.stdout.write("0%\x08\x08\x08 ")
        sys.stdout.flush()
    elif arg[0] == "p": # 25%
        sys.stdout.write("25%\x08\x08\x08\x08 ")
        sys.stdout.flush()
    elif arg[0] == "h": # 50%
        sys.stdout.write("50%\x08\x08\x08\x08 ")
        sys.stdout.flush()
    elif arg[0] == "x": # 75%
        sys.stdout.write("75%\x08\x08\x08\x08 ")
        sys.stdout.flush()


if __name__ == "__main__":

	# disable verbosity by default
    phrase = None
    pfunc = None

	# init the command arg parser
    parser = OptionParser(usage=usage)
	# add option for key type selection
    parser.add_option(
        "-t",
        "--type",
        type="string",
        dest="ktype",
        help="Specify type of key to create (dsa or rsa)",
        metavar="ktype",
        default=default_values["ktype"],
    )
	# add option for key length (bits)
    parser.add_option(
        "-b",
        "--bits",
        type="int",
        dest="bits",
        help="Number of bits in the key to create",
        metavar="bits",
        default=default_values["bits"],
    )
	# add option to specify key encryption password
    parser.add_option(
        "-N",
        "--new-passphrase",
        dest="newphrase",
        help="Provide new passphrase",
        metavar="phrase",
    )
	# add option for old password
    parser.add_option(
        "-P",
        "--old-passphrase",
        dest="oldphrase",
        help="Provide old passphrase",
        metavar="phrase",
    )
	# add option to override default file name
    parser.add_option(
        "-f",
        "--filename",
        type="string",
        dest="filename",
        help="Filename of the key file",
        metavar="filename",
        default=default_values["filename"],
    )
	# add option to silence stdout
    parser.add_option(
        "-q", "--quiet", default=False, action="store_false", help="Quiet"
    )
	# add option to display more information about generation
    parser.add_option(
        "-v", "--verbose", default=False, action="store_true", help="Verbose"
    )
	# add option to append comment to key file
    parser.add_option(
        "-C",
        "--comment",
        type="string",
        dest="comment",
        help="Provide a new comment",
        metavar="comment",
        default=default_values["comment"],
    )

	# create tuple for arguments
    (options, args) = parser.parse_args()

	# if argument count is only 1, then print help and exit
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(0)

	# parse all user options and override default values with them
    for o in list(default_values.keys()):
        globals()[o] = getattr(options, o, default_values[o.lower()])

	# if password enabled, create it
    if options.newphrase:
        phrase = getattr(options, "newphrase")

	# if verbosity enabled, display key information and enable progress callback
    if options.verbose:
        pfunc = progress
		# queue key info to stdout
        sys.stdout.write(
            "Generating priv/pub %s %d bits key pair (%s/%s.pub)..."
            % (ktype, bits, filename, filename)
        )
		# flush all messages so user can see
        sys.stdout.flush()

	# check that DSA key information is correct, if not create exception
    if ktype == "dsa" and bits > 1024:
        raise SSHException("DSA Keys must be 1024 bits")

	# check for valid key algorithm, if not create exception
    if ktype not in key_dispatch_table:
        raise SSHException(
            "Unknown %s algorithm to generate keys pair" % ktype
        )

    # generating private key
    prv = key_dispatch_table[ktype].generate(bits=bits, progress_func=pfunc)
	# write the actual key file with the appropriate name and password
    prv.write_private_key_file(filename, password=phrase)

    # generating public key
    pub = key_dispatch_table[ktype](filename=filename, password=phrase)
	# from the private key, generating matching public key
    with open("%s.pub" % filename, "w") as f:
		# use base64 algorithm to output hash of key
        f.write("%s %s" % (pub.get_name(), pub.get_base64()))
		# append user comment if necessary
        if options.comment:
            f.write(" %s" % comment)

	# let the user know we're finished, if they enabled verbosity
    if options.verbose:
        print("done.")

	# get hexadeceimal hash of our public key
    hash = u(hexlify(pub.get_fingerprint()))
	# print the output
    print(
        "Fingerprint: %d %s %s.pub (%s)"
		# create a tuple with groups of 2 hexadecimal digits for our fingerprint
        % (
            bits,
            ":".join([hash[i : 2 + i] for i in range(0, len(hash), 2)]),
            filename,
            ktype.upper(),
        )
    )
