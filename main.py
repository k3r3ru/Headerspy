import binascii


def revEndian(bytes):
    reversedBytes = []
    for i in range(0, int(len(bytes)/2)):
        readOffset = int(2*i)+2
        readStart = len(bytes) - readOffset
        reversedBytes.append(bytes[readStart:readStart+2])
    return reversedBytes


def xorEnc(d, k):
    for i in range(0, len(d)):
        d[i] = binascii.hexlify(bxor(d[i], k[i % len(k)]))
    return d


def bxor(b1, b2):
    return bytes(x ^ y for (x, y) in zip(b1, b2))


if __name__ == '__main__':
    f = open("/Users/davideangella/Downloads/7z2201-x64.exe", "rb")
    f.seek(128)
    data = revEndian(f.read((4)))
    f.seek(128+84)
    key = revEndian(f.read((4)))
    print(data)
    print(key)
    print(xorEnc(data,key))

