"""
This script is a quick Python 3.8+ implementation of the Python 2 RecentFileCache parser by Patrick Olsen (https://github.com/prolsen/recentfilecache-parser)
The original credits for the bcf file read go to him
Can be used from the commandline or as an import

Author: devsda12
"""

import struct
import sys

class InvalidSignatureException(Exception):
    def __init__(self):
        message = "The provided file is not a valid RecentFileCache file"
        super().__init__(message)

def main():
    try:
        recentfilecache_file = sys.argv[sys.argv.index("-f") + 1]
        parse_rcf(recentfilecache_file)
    except ValueError:
        print("Usage: python py3_rfcparser.py [-h] [-f RecentFileCache.bcf]")


def parse_rcf(input_file):
    try:
        with open(input_file, "rb") as f:
            # Offset
            offset = 0x14
            # Go to beginning of file.
            f.seek(0)
            # Checking if signature is correct
            if (f.read(1) != b'\xfe'):
                raise InvalidSignatureException
            # Read forward 0x14 (20).
            f.seek(offset)

            #Instantiating the return list
            returnlist = []

            # Reading one byte, if it's empty break the loop
            while (curread:= f.read(1)):
                #Reading 3 bytes
                f.read(3)

                #Checking what the length is of the next value
                rl = struct.unpack('>B', curread)[0]
                fnlen = (rl + 1) * 2

                #Retrieving the actual value
                foundpath = f.read(fnlen).replace(b'\x00', b'').decode()
                print(foundpath)
                returnlist.append(foundpath)

            return returnlist
    except FileNotFoundError:
        print("Specified file not found")

if(__name__ == "__main__"):
    main()