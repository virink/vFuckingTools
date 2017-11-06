#!/usr/bin/env python3
# -*- encoding: utf-8 -*-

'''
Title : Hex
Author : Virink
Type : crypto
Detail : 16进制编码/解码
Param : @s
'''
import binascii


def encode(s):
    return binascii.hexlify(s.encode('utf-8'))


def decode(s):
    return binascii.unhexlify(s).decode('utf-8')

if __name__ == '__main__':
    TEST = 'Hello,世界'
    print(encode(TEST))
    print(decode(encode(TEST)))
