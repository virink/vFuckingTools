# -*- coding:utf8 -*-
import sys
from Crypto.Cipher import AES


def decrypt_aes(key, data):
    obj = AES.new(key, AES.MODE_ECB)
    return obj.decrypt(data)

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("%s key encrypt" % sys.argv[0])
        return False
    key = sys.argv[1]
    data = open(sys.argv[2], 'rb').read()
    print(decrypt_aes(key, data))
