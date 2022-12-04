import binascii
from translateVersions import *
import sys


def swapBytes(b, nbytes):
    bint = int.from_bytes(b, byteorder="little", signed=False)
    return bint.to_bytes(nbytes, byteorder="big", signed=False)


def bxor(b1, b2):
    return bytes(x ^ y for (x, y) in zip(b1, b2))


def parseRH(fPath):
    f = open(fPath, "rb")

    f.seek(212)
    key = swapBytes(f.read(4), 4)
    print("------------------------")
    print("| XOR KEY: " + str(binascii.hexlify(key)) + " |")
    print("------------------------")

    f.seek(128)
    print("+ DanS ID: " + str(binascii.hexlify(bxor(swapBytes(f.read(4), 4), key))))

    for i in range(0,7):
        f.seek(128 + 16 + i*8)
        data = swapBytes(f.read(8), 8)
        xoredData = str(binascii.hexlify(data))
        unxored = str(binascii.hexlify(bxor(data[:4], key)[-2:] + bxor(data[4:], key)))
        prod = prodID[binascii.hexlify(bxor(data, key)[2:4])]
        build = str(int(unxored[10:14], 16))
        vers = translateCompiler(binascii.hexlify(bxor(data[4:], key)[:2]))

        print("+ Data: {} - Un-XORed: {} - Prod ID: {} - Build ID: {} - Version: {}".format(
            xoredData,
            unxored,
            prod,
            build,
            vers
        ))


try:
    path = sys.argv[1]
    parseRH(path)
except:
    print("Error opening the PE. Please check the submitted file path")
    sys.exit(1)